; This file is part of OpenGossip.
;
; This program is free software: you can redistribute it and/or modify it
; under the terms of the GNU Lesser General Public License as published by
; the Free Software Foundation, either version 3 of the License, or (at your
; option) any later version.  This program is distributed in the hope that it
; will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
; of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser
; General Public License for more details.  You should have received a copy
; of the GNU Lesser General Public License along with this program.  If not,
; see <http://www.gnu.org/licenses/>.

(ns mg.core
  "<M>ultivariate <G>aussian computation"
  (:gen-class)
  (:require [incanter.core   :refer :all :as core]
            [incanter.stats  :refer :all :as stats]
            [incanter.io     :refer :all :as io]
            [incanter.charts :refer :all :as charts]))

; Outlier detection threshold.
(def default-threshold 1e-05)

(defn estimate-gaussian
  "Returns gaussian parameters mu (mean vector) and sigma (covariance
  matrix) of the input `X` matrix."
  [X]
  (let [[m n] (core/dim X)
        mu (div (reduce plus X) m)
        sigma (stats/covariance X)]
    [mu sigma]))

(defn pinv
  "Returns the pseudoinverse of a matrix `X`; the coefficient vector
  of OLS is the dependent variable vector premultiplied by the
  pseudoinverse of the cofactor matrix `X`."
  [X]
  {:pre [(core/matrix? X)]}
  (let [Xt  (core/trans X)
        XtX (core/mmult Xt X)]
    (mmult (core/solve X) Xt)))

(defn multivariate-normal
  "Computes the multivariate gaussian.
     X:      input vectors (m x n)
     mu:     means vector (n x 1)
     sigma:  covariance matrix (n x n)"
  [X mu sigma]
  (let [n  (core/length mu)
        MU (repeat (core/nrow X) mu)
        X  (core/minus X MU)]
    (core/mult
     (Math/pow (* 2 Math/PI) (/ (- n) 2))
     (Math/pow (core/det sigma) -0.5)
     (exp
      (core/mult -0.5 (map core/sum (mult (core/mmult X (pinv sigma)) X)))))))

(defn agg
  "Computes aggregation of `metric', using function `fn' on dataset `ds'.
  Uses a unique column identifier to join sets without name conflicts."
  [metric fn ds]
  (core/rename-cols
   {:val (keyword (subs (str fn "-" metric) 1))} ; strip leading ':'
   ($rollup fn :val :host ds)))

(defn aggegations
  "Returns list of aggregated results for each host. This currently mostly
  gives LAPACK DGESV issues (ie. a non reversible matrix)."
  [metric ds]
  (reduce
   (partial $join [:host :host])
   [(agg metric :sum ds)
    (agg metric :min ds)
    (agg metric :max ds)]))

(defn columns-in-order
  "Returns a list of expected columns order. Put :host as first column and
   append the rest."
  [cols]
  (cons :host (filter #(not= :host %) cols)))

(defn prepare-data
  "Read OpenTSDB output file and build the matrix of numbers with metrics,
  hosts and values. Returns a hash-map with :metrics, :hosts and :data as
  keys."
  [file]
  (let [ds      ($ [0 2 3]
                   (io/read-dataset file :delim \space :header false))
        metrics (zipmap (distinct ($ 0 ds)) (range))
        hosts   (zipmap (distinct ($ 2 ds)) (range))]
    {:metrics metrics,
     :hosts hosts,
     :data (core/rename-cols
      {:col-0 :metric, :col-1 :host, :col-2 :val}
      (core/conj-cols
       ($map #(get metrics %) :col0 ds)
       ($map #(get hosts %) :col3 ds)
       ($ 1 ds)))}))

(defn group-data
  "Build a dataset, grouped by each metric, with 1 row per host where all
  the features of the metric is computed (sum, mean...)."
  [ds]
  (let [groups ($group-by :metric ds)]
    (into (empty groups)
          (for [[k v] groups]
            {k (agg (:metric k) :mean v)}))))

(defn summarize-data
  "Build the matrix from input dataset."
  [ds]
  (let [groups (group-data ds)
        grid   (reduce (partial $join [:host :host]) (vals groups))]
    (core/to-matrix
     (core/reorder-columns grid (columns-in-order (core/col-names grid))))))

(defn keep-features
  "Returns the summarized-data matrix without the 'host' columns, just keep
  the features values."
  [X]
  ($ (rest (range (ncol X))) X))

(defn rescale-feature
  "Returns a rescaled sequence of values (belongs to [0, 1])."
  [X]
  (let [Xmin    (reduce min X) ; TODO: Compute both min and max
        Xmax    (reduce max X) ; in a single step.
        Xdiff   (- Xmax Xmin)
        rescale (fn [x]
                  (if (== Xdiff 0.0) 0.0 (float (/ (- x Xmin) Xdiff))))]
    (map rescale X)))

(defn rescale-matrix
  "Rescale all the features of input matrix."
  [X]
  (core/to-matrix
   (reduce core/conj-cols
           (map #(rescale-feature ($ % X)) (range (core/ncol X))))))

(defn mark-outliers
  "Returns the input list of m elements with true if element is an outlier,
  false otherwise."
  [p epsilon]
  (seq (map (partial > epsilon) p)))

(defn extract-outliers
  "Returns list of nodes considered as outliers."
  [p X epsilon]
  (let [mapped   (core/to-matrix (core/conj-cols p X))
        outliers (filter #(> epsilon (sel % :cols 0 :rows 0)) mapped)]
    (core/rename-cols
     {:col-0 :p, :col-1 :host}
     (core/to-dataset
      (reduce core/conj-rows outliers) :transpose true))))

(defn view-outliers
  "Display results on a grid.
     X1:     Values for x1 axis
     X2:     Values for x2 axis
     states: Vector of boolean (true = outlier)"
  [X1 X2 states]
  {:pre [(= (dim X1) (dim X2))]}
  (let [plot (charts/scatter-plot X1 X2 :group-by states)]
    (core/save plot "/tmp/test.png") ; TODO Don't hardcorde...
    (core/view plot)))

(defn view-feature
  "Display histogram of input feature (m x 1 vector)."
  [serie name]
  (do
    (view (charts/histogram serie :title name))))

(defn process
  "Process input OpenTSDB file, find and display outliers."
  [filename threshold]
  (let [data       (prepare-data filename)
        A          (summarize-data (:data data))
        B          (keep-features A)
        X          (rescale-matrix B)
        [mu sigma] (estimate-gaussian X)
        p0         (multivariate-normal X mu sigma)
        p          (rescale-feature p0)
        states     (mark-outliers p threshold)
        X1         ($ 0 B) ; TODO Chose which features to use to
        X2         ($ 1 B) ; display charts. PCA?
        outliers   (extract-outliers p A threshold)
        hosts      (clojure.set/map-invert (:hosts data))]
    (dorun
     (for [[k v] (:metrics data)]
       (view-feature ($ v B) k)))
    (view-feature p "p(X)")
    (view-outliers X1 X2 states)
    (println "Outliers: "
             (nrow outliers)
             (core/conj-cols ($ :p outliers)
                             ($map #(get hosts (int %)) :host outliers)))))

(defn -main [& args]
  (case (count args)
    0 (println "Usage: program <filepath> [threshold]")
    1 (process (first args) default-threshold)
    2 (process (first args) (read-string (nth args 1)))))
