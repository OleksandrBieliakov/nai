from common import read_file, Sample
import random
from math import log2


def find_distance(attributes1, attributes2):
    distance = 0
    for x, y in zip(attributes1, attributes2):
        distance += (x - y) ** 2
    return distance


def assign_random_clusters_to_samples(samples, k):
    clusters = dict()
    for i in range(k):
        clusters[i] = list()
    for sample in samples:
        sample.cluster = random.randrange(k)
        clusters[sample.cluster].append(sample)
    return clusters


def is_assigned_ok(clusters, k):
    for i in range(k):
        if len(clusters[i]) == 0:
            return False
    return True


def calculate_centroids(clusters, k, num_of_attributes):
    centroids = list()
    for i in range(k):
        cluster_samples = clusters[i]
        sum_of_attributes = [0] * num_of_attributes
        for sample in cluster_samples:
            for j in range(num_of_attributes):
                sum_of_attributes[j] += sample.attributes[j]
        means_of_attributes = [0] * num_of_attributes
        for n in range(num_of_attributes):
            if len(cluster_samples) != 0:
                means_of_attributes[n] = sum_of_attributes[n] / len(cluster_samples)
        centroids.append(Sample(means_of_attributes, cluster=i))
    return centroids


def assign_samples_to_nearest_centroids(samples, centroids):
    clusters = dict()
    for i in range(len(centroids)):
        clusters[i] = list()
    for sample in samples:
        min_distance = find_distance(sample.attributes, centroids[0].attributes)
        min_centroid = centroids[0]
        for i in range(1, len(centroids)):
            distance = find_distance(sample.attributes, centroids[i].attributes)
            if distance < min_distance:
                min_distance = distance
                min_centroid = centroids[i]
        sample.cluster = min_centroid.cluster
        clusters[sample.cluster].append(sample)
    return clusters


def sums_of_distances_to_centroids(centroids, clusters):
    sums = dict()
    total = 0
    for i in range(len(clusters)):
        sum = 0
        for sample in clusters[i]:
            distance = find_distance(sample.attributes, centroids[i].attributes)
            sample.distance = distance
            sum += distance
        sums[i] = int(sum)
        total += int(sum)
    return sums, total


def calculate_entropy(cluster):
    classes_counters = dict()
    for sample in cluster:
        if sample.decision in classes_counters:
            classes_counters[sample.decision] = classes_counters[sample.decision] + 1
        else:
            classes_counters[sample.decision] = 1
    probabilities = dict()
    for sample_class in classes_counters.keys():
        if len(cluster) != 0:
            probabilities[sample_class] = classes_counters[sample_class] / len(cluster)
    entropy = 0.
    for probability in probabilities.values():
        entropy += probability * log2(probability)
    if entropy != 0:
        entropy *= -1
    return classes_counters, entropy


test_path = "iris_test.txt"
training_path = "iris_training.txt"
test_samples = read_file(training_path)
num_of_attributes = len(test_samples[0].attributes)

print("Enter parameter k:")
k = int(input())

clusters = assign_random_clusters_to_samples(test_samples, k)
while not is_assigned_ok(clusters, k):
    clusters = assign_random_clusters_to_samples(test_samples, k)

max_iterations = 100
iterations_counter = 0
previous_sums = None
print("\nSums of distances at each iteration:")
for i in range(max_iterations):
    centroids = calculate_centroids(clusters, k, num_of_attributes)
    clusters = assign_samples_to_nearest_centroids(test_samples, centroids)
    sums, total = sums_of_distances_to_centroids(centroids, clusters)
    print(i + 1, sums, "total", total)
    iterations_counter += 1
    if sums == previous_sums:
        break
    previous_sums = sums

print("\nAfter", iterations_counter, "iterations:")
for i in range(k):
    print("Cluster", i)
    classes_counters, entropy = calculate_entropy(clusters[i])
    print("counters:", classes_counters, "total", len(clusters[i]))
    print("entropy:", "{:.2}".format(entropy))
    #for sample in clusters[i]:
    #    print(sample)
    print()
