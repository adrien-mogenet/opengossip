(ns mg.core-test
  (:require [clojure.test :refer :all]
            [mg.core :refer :all])
  (:use (incanter core stats io charts)))

; 3x3 matrix
(def M-1     (matrix [[1.0  2.0  3.0]
                      [4.0  5.0  6.0]
                      [7.0  8.0  9.0]]))

; mean vector of M-1
(def mu-1             [4.0  5.0  6.0])

; covariance matrix of M-1
(def sigma-1 (matrix [[9.0  9.0  9.0]
                      [9.0  9.0  9.0]
                      [9.0  9.0  9.0]]))

; what we should get when reading test-00.csv
(def expected-ds
  (rename-cols
   {:col-0 :metric, :col-1 :host, :col-2 :val}
   (to-dataset
    [[0 0 3.0]
     [0 1 4.0]
     [0 2 5.0]
     [1 0 5.0]
     [1 2 2.0]
     [1 1 6.0]])))

; host, sum metric1, sum metric2
(def expected-matrix
  (matrix
   [[1 6 4]
    [2 2 5]
    [0 5 3]]))

; without host column
(def feature-matrix
  (matrix
   [[6 4]
    [2 5]
    [5 3]]))

(deftest test-build-matrix
  (testing "build matrix"
    (let [data (prepare-data "samples/test-00.csv")]
      (is (= expected-ds (:data data)))
      (is (= 2 (count (:metrics data))))
      (is (= 3 (count (:hosts data)))))))

(deftest test-group-data
  (testing "group-data"
    (is (= 2
           (count (group-data expected-ds))))))

(deftest test-summarize-data
  (testing "summarize-data"
    (is (= expected-matrix
           (summarize-data expected-ds)))))

(deftest test-keep-feature
  (testing "remove host column"
    (is (= feature-matrix
           (keep-features expected-matrix)))))

(deftest test-gaussian-estimation
  (testing "basic"
    (is (= [mu-1 sigma-1]
           (estimate-gaussian M-1))))
  (testing "real dataset"
    (let [mu    (matrix [[(/ 13 3) 4.0]])
          sigma (matrix [[(/ 13 3) -1.50]
                         [-1.50     1.00]])]
      (is (= [mu sigma]
             (estimate-gaussian feature-matrix))))))

(deftest test-multivariate-normal
  (testing "real dataset"
    (let [[mu sigma] (estimate-gaussian feature-matrix)]
      (is (= [3 1] (dim (multivariate-normal feature-matrix mu sigma)))))))

(deftest test-mark-outliers
  (testing "mark-outliers"
    (let [[mu sigma] (estimate-gaussian feature-matrix)
          p          (multivariate-normal feature-matrix mu sigma)]
      (is (= [false true false]
             (mark-outliers p 1e-02))))))

(deftest test-extract-outliers
  (testing "extract-outliers")
      (let [[mu sigma] (estimate-gaussian feature-matrix)
            p          (multivariate-normal feature-matrix mu sigma)
            result     (extract-outliers p expected-matrix 1e-02)]
        (println result)
        (is (= [1 4] (dim result)))))

(deftest test-rescale-feature
  (testing "basic scaling features"
    (is (= [0.5  0.0  1.0]
           (rescale-feature [100 50 150]))))
  (testing "unique value"
    (is (= [0.0  0.0  0.0]
           (rescale-feature [32 32 32])))))

(deftest test-rescale-matrix
  (testing "rescale-matrix"
    (is (= (matrix [[0.5  1.0]
                    [0.0  0.5]
                    [1.0  0.0]])
           (rescale-matrix (matrix [[100  15]
                                    [ 50  10]
                                    [150   5]]))))))
