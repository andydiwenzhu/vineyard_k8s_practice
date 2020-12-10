# example of distributed learning with mars and pytorch

First we use mars to preprocess the raw data that are stored in
hdfs, and save the resulted dataframe in vineyard. Note that the
mars session is lauched in k8s.

Then we conduct distributed learning with pytorch, we build the training
code into an image, and launch k8s pods for distributed learning. Each pod
will fetch the corresponding dataframe partition for its training, in case
the data partition is miss-scheduled, vineyard will automatically migration
the data partition when allow_migration is set to True.

