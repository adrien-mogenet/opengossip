#!/usr/bin/env octave-cli -q

# This file is part of OpenGossip.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser
# General Public License for more details.  You should have received a copy
# of the GNU Lesser General Public License along with this program.  If not,
# see <http://www.gnu.org/licenses/>.

function visualizeFit(X, mu, Sigma, dim=2)
  # Displays the contours for our computed gaussian:
  #  - X: input vectors (m x n), only used to plot points
  #  - mu: means vector (n x 1)
  #  - Sigma: covariance matrix (n x n)
  # Note that n=2 when plotting.
  [X1, X2] = meshgrid(-1:.5:20);
  Z = multivariateGaussian([X1(:) X2(:)], mu, Sigma);
  Z = reshape(Z, size(X1));
  if dim == 2
    plot(X(:, 1), X(:, 2), 'bx');
    hold on;
    # Do not plot if there are infinities
    if (sum(isinf(Z)) == 0)
      contour(X1, X2, Z, 10.^(-50:3:0)');
    end
  elseif dim == 3
    p = multivariateGaussian(X, mu, Sigma);
    plot3(X(:, 1), X(:, 2), p, 'bx');
    hold on;
    if (sum(isinf(Z)) == 0)
      contour3(X1, X2, Z, 10.^(-50:3:0)');
    end
  end
  hold off;
end

function visualizeOutliers(X, mu, Sigma, epsilon, dim=2)
  # Find anomalies and plot them
  #  - X: input vectors (m x n)
  #  - mu: means vector (n x 1)
  #  - Sigma: covariance matrix (n x n)
  #  - epsilon: threshold
  p = multivariateGaussian(X, mu, Sigma);
  outliers = find(p < epsilon);
  csvwrite('anomalies.txt', outliers)
  fprintf("%d anomalies have been detected\n", length(outliers))
  hold on
  if dim == 2
    plot(X(outliers, 1), X(outliers, 2), 'ro', 'LineWidth', 2,
         'MarkerSize', 10);
  elseif dim == 3
    plot3(X(outliers, 1), X(outliers, 2), p(outliers), 'ro',
          'LineWidth', 2,  'MarkerSize', 10);
  end
  hold off
end

function [mu Sigma] = estimateGaussian(X)
  # Returns the gaussian parameters:
  #   - X: the input vectors (m x n)
  #
  # Returns:
  #   - mu: the means vector (n x 1)
  #   - Sigma: the covariance matrix (n x n)
  [m, n] = size(X);
  mu = sum(X) / m;
  Sigma = cov(X, X, 1);
end

function p = multivariateGaussian(X, mu, Sigma)
  # Computes the multivariate gaussian
  #  - X: input vectors (m x n)
  #  - mu: means vector (n x 1)
  #  - Sigma: covariance matrix (n x n)
  n = length(mu);
  if (size(Sigma, 2) == 1) || (size(Sigma, 1) == 1)
    Sigma = diag(Sigma);
  end
  X = bsxfun(@minus, X, mu(:)');
  p = (2 * pi) ^ (- n / 2) * det(Sigma) ^ (-0.5) * ...
      exp(-0.5 * sum(bsxfun(@times, X * pinv(Sigma), X), 2));
end


# m: size of training set
# n: number of features
#
# Input file is a [m x n] matrix
if (length(argv()) == 0)
  printf("Usage: %s <input file>", program_name())
  exit
end
input_file = argv(){1};
data = load('-ascii', input_file);

# Threshold to detect anomalies
EPSILON = 0.005;

# Plotting dimensions
DIMENSIONS = 3;

# Give sense to our features
compaction_queue = data(:, 1);
ios_in_progress = data(:, 2);
loadavg = data(:, 3);
meminfo_active = data(:, 4);
meminfo_swap = data(:, 5);

# Perform some feature scaling to adjust gaussian distribution
meminfo_swap = (log(meminfo_swap) ./ 4) .^ 2.5;
loadavg = loadavg .* 10;

# Build vector we'll use later and compute gaussian parameters
X = [loadavg meminfo_swap];
[mu Sigma] = estimateGaussian(X);

# Plot everything
visualizeFit(X,  mu, Sigma, DIMENSIONS);
visualizeOutliers(X, mu, Sigma, EPSILON, DIMENSIONS)
xlabel('loadavg * 10');
ylabel('log(swap)');
print -deps result.eps
