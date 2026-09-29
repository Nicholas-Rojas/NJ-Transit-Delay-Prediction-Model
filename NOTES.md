=== BASELINE ===
Accuracy: 0.7349
(precision/recall/F1 are 0 - it never predicts a delay)

======= MODEL TESTING WITH & WITHOUT WEATHER FEATURES LGMCLASSIFIER USING CLASS_WEIGHT = "BALANCED" =========

=== NO WEATHER ===
Accuracy:  0.5601
Precision: 0.3564
Recall:    0.819
F1:        0.4967
Confusion:
 [[300616 343505]
 [ 42051 190247]]
Top 10 features:
 from             2546
hour             1258
line              637
stop_sequence     613
dayofweek         514
month             432
is_weekend          0
dtype: int32

=== WITH WEATHER ===
Accuracy:  0.5728
Precision: 0.359
Recall:    0.7788
F1:        0.4914
Confusion:
 [[321054 323067]
 [ 51378 180920]]
Top 10 features:
 from              2288
hour              1013
line               583
stop_sequence      509
dayofweek          494
month              397
temperature_2m     335
windgusts_10m      191
precipitation       74
snow_depth          67
dtype: int32


========= CLASS_WEIGHT NOT INCLUDED =========

=== NO WEATHER ===
Accuracy:  0.7458
Precision: 0.5469
Recall:    0.2383
F1:        0.3319
Confusion:
 [[598268  45853]
 [176948  55350]]


Top 10 features:
 from             2568
hour             1238
line              648
stop_sequence     610
dayofweek         497
month             439
is_weekend          0
dtype: int32


=== WITH WEATHER ===
Accuracy:  0.7388
Precision: 0.5182
Recall:    0.209
F1:        0.2979
Confusion:
 [[598968  45153]
 [183738  48560]]
Top 10 features:


from              2207
hour              1034
line               582
dayofweek          510
stop_sequence      498
month              402
temperature_2m     378
windgusts_10m      189
snow_depth          77
precipitation       70
dtype: int32