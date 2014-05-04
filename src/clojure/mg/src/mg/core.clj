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
  (:require [incanter.core :refer :all]
            [incanter.stats :refer :all]
            [incanter.io :refer :all]
            [incanter.charts :refer :all]))

; Outlier detection threshold.
(def threshold 1e-07)

(defn join-all
  "Join several datasets `ds' all together by their key `k'"
  [k ds]
  "fixme")

(defn estimate-gaussian
  "Returns gaussian parameters mu (mean vector) and sigma (covariance
  matrix) of the input `X` matrix."
  [X]
  (let [[m n] (dim X)
        mu (div (reduce plus X) m)
        sigma (covariance X)]
    [mu sigma]))

(defn pinv
  "Returns the pseudoinverse of a matrix `X`; the coefficient vector
  of OLS is the dependent variable vector premultiplied by the
  pseudoinverse of the cofactor matrix `X`."
  [X]
  {:pre [(matrix? X)]}
  (let [Xt (trans X)]
    (mmult (solve (mmult Xt X)) Xt)))

(defn multivariate-normal
  "Computes the multivariate gaussian.
     X:      input vectors (m x n)
     mu:     means vector (n x 1)
     sigma:  covariance matrix (n x n)"
  [X mu sigma]
  (let [n  (length mu)
        MU (repeat (nrow X) mu)
        X  (minus X MU)]
    (mult
     (Math/pow (* 2 Math/PI) (/ (- n) 2))
     (Math/pow (det sigma) -0.5)
     (exp (mult -0.5 (map sum (mult (mmult X (pinv sigma)) X)))))))

(defn parse-file
  "Parse a CSV file and build the matrix"
  [filename]
  (let [ds (rename-cols
            {:col0 :metric :col1 :ts :col2 :val :col3 :host}
            (read-dataset filename :delim \space :header false))
        ; aggregate :val, group by :host
        ds-max  (rename-cols {:val :max} ($rollup :max :val :host ds))
        ds-min  (rename-cols {:val :min} ($rollup :min :val :host ds))
        ds-mean (rename-cols {:val :mean} ($rollup :mean :val :host ds))]
    (to-matrix
     ($join [:host :host] ds-mean
            ($join [:host :host] ds-max ds-min)))))

(defn extract-outliers
  "Returns list of nodes considered as outliers."
  [p X]
  (rename-cols
   {:col-0 :p, :col-3 :host}
   (reduce conj-rows (filter
                      #(> threshold (sel % :cols 0 :rows 0))
                      (to-matrix (conj-cols p X))))))

(defn view-results
  "Display results on a grid.
     X1:     Values for x1 axis
     X2:     Values for x2 axis
     groups: Vector of boolean (true = outlier)"
  [X1 X2 groups]
  {:pre [(= (dim X1) (dim X2))]}
  (view (scatter-plot X1 X2 :group-by groups)))

(defn process
  "Process input CSV file, find and display outliers."
  [filename]
  (let [X          (parse-file filename)
        [mu sigma] (estimate-gaussian X)
        p          (multivariate-normal X mu sigma)
        groups     (map (partial < threshold) p)
        X1         (sel X :cols 0)
        X2         (sel X :cols 1)]
    (view-results X1 X2 groups)
    (println (extract-outliers p X))))

(defn -main [& args]
  (process (first args)))
