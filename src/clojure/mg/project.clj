(defproject mg "0.1.0-SNAPSHOT"
  :description "Multivariate Gaussian using Incanter"
  :url "https://github.com/adrien-mogenet/opengossip"
  :main mg.core
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}
  :dependencies [[org.clojure/clojure "1.5.1"]
                 [incanter/incanter-core "1.5.5"]
                 [incanter/incanter-io "1.5.5"]
                 [incanter/incanter-charts "1.5.5"]]
  :jvm-opts ["-Xmx512M"
             "-XX:+TieredCompilation"
             "-XX:TieredStopAtLevel=1"])
