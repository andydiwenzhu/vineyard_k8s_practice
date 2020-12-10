import vineyard
import mars
import mars.dataframe as md

vineyard_deployment = vineyard.connect('vineyard-k8s-service')

# this create a default session for mars
# so that following operations are applied
# within the scope of the session
mars.session(vineyard_deployment)

dataset = md.from_vineyard(vineyard.io.stream.open('hdfs://server/data_full'))

df = dataset.dropna().filter(condition).vectorize(method).to_vineyard()
