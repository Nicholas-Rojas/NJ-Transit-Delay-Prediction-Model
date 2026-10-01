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




======== TESTING/ANALYZING AMTRAK SCHEDULE ==========

Name: count, dtype: int64 

Non-NJT rows: 12322 (4.8% of file)

=== top Amtrak stations ===
from
Philadelphia             2758
Newark Penn Station      2722
New York Penn Station    2692
Trenton                  1971
Metropark                1363
Newark Airport            599
Princeton Junction        140
New Brunswick              61
Secaucus Lower Lvl          2
Ridgewood                   1
Ramsey Route 17             1
Waldwick                    1
Allendale                   1
Ramsey Main St              1
Ho-Ho-Kus                   1
Name: count, dtype: int64 

=== sample Amtrak rows ===
   train_id    type      line                 from scheduled_time
35     A186  Amtrak  REGIONAL         Philadelphia            NaN
36     A186  Amtrak  REGIONAL         Philadelphia            NaN
37     A186  Amtrak  REGIONAL              Trenton            NaN
38     A186  Amtrak  REGIONAL            Metropark            NaN
39     A186  Amtrak  REGIONAL       Newark Airport            NaN
40     A186  Amtrak  REGIONAL  Newark Penn Station            NaN
41     A172  Amtrak  REGIONAL         Philadelphia            NaN
42     A172  Amtrak  REGIONAL         Philadelphia            NaN
43     A172  Amtrak  REGIONAL              Trenton            NaN
44     A172  Amtrak  REGIONAL            Metropark            NaN

Amtrak rows: 12322
scheduled_time populated: 0.0
actual_time populated:    1.0
delay_minutes populated:  0.0
date populated:           1.0


          date scheduled_time          actual_time  delay_minutes
35  2018-03-01            NaN  2018-03-01 15:01:14            NaN
36  2018-03-01            NaN  2018-03-01 15:33:13            NaN
37  2018-03-01            NaN  2018-03-01 15:55:14            NaN
38  2018-03-01            NaN  2018-03-01 16:06:15            NaN
39  2018-03-01            NaN  2018-03-01 16:12:16            NaN
40  2018-03-01            NaN  2018-03-01 16:30:14            NaN
41  2018-03-01            NaN  2018-03-01 09:19:10            NaN
42  2018-03-01            NaN  2018-03-01 09:49:07            NaN


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



=== BASE + WEATHER + AMTRAK ===
Accuracy:  0.5718
Precision: 0.3589
Recall:    0.783
F1:        0.4922
Confusion:
 [[319200 324921]
 [ 50401 181897]]
Top 10 features:
 from              2242
hour              1018
line               613
stop_sequence      497
dayofweek          479
month              402
temperature_2m     339
windgusts_10m      178
precipitation       75
snow_depth   

## Checking if data actually contains prev_delay or possible leakage

        train_id        date  stop_sequence  delay_minutes  prev_delay
2627209     0041  2018-03-01            1.0       0.000000         NaN
2627210     0041  2018-03-01            2.0       2.083333    0.000000
2627211     0041  2018-03-01            3.0       2.150000    2.083333
2627212     0041  2018-03-01            4.0       1.066667    2.150000
2627213     0041  2018-03-01            5.0       1.100000    1.066667
2627214     0041  2018-03-01            6.0       1.183333    1.100000
2627215     0041  2018-03-01            7.0       1.150000    1.183333
2627216     0041  2018-03-01            8.0       0.100000    1.150000



=== BASE + PREV_DELAY + WEATHER + AMTRAK ===
Accuracy:  0.8855
Precision: 0.7517
Recall:    0.8483
F1:        0.7971
Confusion:
 [[579013  65108]
 [ 35235 197063]]
Top 10 features:
 from              2876
prev_delay        1049
stop_sequence      734
hour               555
line               285
dayofweek          197
month              165
temperature_2m      61
amtrak_count        34
snowfall            17
dtype: int32




=== BASE + PREV_DELAY ===
Accuracy:  0.8867
Precision: 0.7544
Recall:    0.8487
F1:        0.7988
Confusion:
 [[579956  64165]
 [ 35156 197142]]
Top 10 features:
 from             2891
prev_delay       1034
stop_sequence     789
hour              593
line              324
month             189
dayofweek         180
is_weekend          0
dtype: int32



## Cross Reference Results


congestion table shape: (93018, 3)
count    93018.000000
mean         3.353104
std          2.213167
min          1.000000
25%          2.000000
50%          3.000000
75%          5.000000
max         20.000000
Name: amtrak_count, dtype: float64

busiest station-hours:
                        from            datehour  amtrak_count
61693           Philadelphia 2018-08-22 15:00:00            20
21092  New York Penn Station 2018-08-22 15:00:00            20
24393  New York Penn Station 2019-02-13 07:00:00            19
46045    Newark Penn Station 2018-08-22 15:00:00            19
24673  New York Penn Station 2019-02-27 15:00:00            15