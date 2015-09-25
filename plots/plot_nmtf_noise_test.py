"""
Plot the performances of the many different NMTF algorithms in a single graph.

We plot the average performance across all 10 attempts for different fractions:
[0.1, 0.2, ..., 0.9].

We use a dataset of I=100, J=80, K=5, L=5, with unit mean priors and zero mean 
unit variance noise.

We have the following methods:
- VB NMTF
- Gibbs NMTF

"""

import matplotlib.pyplot as plt
metrics = ['MSE','R^2','Rp']

noise_ratios = [ 0, 0.01, 0.05, 0.1, 0.2, 0.5, 1. ]

# VB NMTF
vb_all_performances = {'R^2': [[0.9999780246042494, 0.9999728206204453, 0.9984911490230137, 0.9981944545191914, 0.9999252480813313, 0.9983356885885295, 0.9999767601683791, 0.9999701765719389, 0.9999824088786982, 0.9968165212265458], [0.9875653506632287, 0.9896511225598952, 0.9899235552328136, 0.9885333476284232, 0.9879348453305571, 0.9872195171849458, 0.9865257197139082, 0.991332209267547, 0.9852870497464197, 0.9883031854270494], [0.9430815111115198, 0.9457909513663281, 0.9457764740543209, 0.9452979800191594, 0.9387595947780062, 0.9473626785122735, 0.9459561681940648, 0.9391055736965196, 0.9356321423187044, 0.9475666623591881], [0.894856992025629, 0.8855450028251782, 0.8786551479922323, 0.8797028516263825, 0.8963286014736116, 0.8854012152942226, 0.8992465416692355, 0.9117406351652049, 0.8709494876270475, 0.8901348595400489], [0.7667474941551151, 0.8001506008456275, 0.7930121788461535, 0.8250564527482962, 0.8405825826123153, 0.823595059062261, 0.8176243675484859, 0.8409875018983681, 0.8443928594850312, 0.8353685167327048], [0.6459181548192321, 0.6385939528974371, 0.6175887074995832, 0.5747917390042832, 0.6482465832591162, 0.5765255687116944, 0.5978887915754144, 0.6597283641615764, 0.624243219495306, 0.5959217348123875], [0.49811502691332643, 0.40532204288540896, 0.4303607912720805, 0.44996183944661805, 0.42171457283420644, 0.46824369954268563, 0.5080909837547092, 0.46883525276725657, 0.4547480132647319, 0.5392824507835542]], 'MSE': [[0.012253433029757042, 0.01217298181368371, 0.85613479079116073, 1.1844714406373891, 0.041099415971386166, 1.1571845945233061, 0.016184878693976935, 0.016238392833694236, 0.010976197662280036, 1.7064918931277142], [7.6507947238156717, 6.669962268576735, 6.7427737572575559, 7.0011443557598305, 6.9723643049651107, 6.5603074199812852, 7.0139435644943635, 6.4104494267509029, 7.5059740007498092, 6.015671422343484], [32.928811524158434, 32.666843173383569, 34.65162463220566, 30.94059224809796, 32.530455557805652, 34.496475950245134, 33.877791425707997, 33.114546791603331, 35.668349734558021, 32.52821201264134], [61.824683187755234, 73.296856563938348, 65.082413213945017, 64.374913632437753, 63.680542994874223, 62.826486287166745, 66.043054283328416, 66.50344077819004, 70.204086150734753, 66.634633909749994], [133.97195262017132, 127.55478153740894, 141.83766838983408, 115.03836435420527, 132.81252466517336, 129.08851512811532, 131.09946035051158, 125.0621776100672, 113.0263764915594, 117.91315795913546], [346.85031257786505, 306.41046814999908, 311.59672919568658, 324.52901751124296, 299.80277373982005, 353.33154582537782, 307.41695818646474, 313.25903123512865, 316.01169164069404, 316.58867322442541], [575.40673344474988, 613.10987995192011, 610.66400699245787, 632.4522024808324, 606.44998819950956, 650.41492741041316, 611.18224939575498, 604.73489905601355, 565.62254975420421, 557.16850864753405]], 'Rp': [[0.99998901814205543, 0.99998646833150662, 0.99925047184688365, 0.99909923589317595, 0.99996271318608987, 0.99917259138068149, 0.99998866790182539, 0.99998535499631402, 0.99999126774893066, 0.99840751441890618], [0.99377066477245213, 0.99481744813298445, 0.99495237365103695, 0.99425528452483469, 0.99395209930695483, 0.99365123448265424, 0.99325459639250524, 0.99566852810673201, 0.99267555694429443, 0.99415588639212726], [0.97194174572865277, 0.97320676512923976, 0.97279985641336209, 0.9723782629958363, 0.96944520536089929, 0.9739533961436595, 0.97430530481757871, 0.96958761389403358, 0.96900053579897605, 0.97393107971659298], [0.94753755910304049, 0.94381006711899396, 0.94042156018897416, 0.93969751331944917, 0.94802941572824717, 0.94141969445241347, 0.95250150846740933, 0.95729968002897214, 0.93496669229047324, 0.94525106150938309], [0.88674898033427552, 0.89571851200756269, 0.89558057436549199, 0.90954865170982468, 0.92141398794594653, 0.90970670059312786, 0.90614624147116885, 0.91802778807470053, 0.92002717463195327, 0.91557595219251509], [0.80377037270812957, 0.79995350449355351, 0.78900128884681109, 0.7583647610612454, 0.80554611018462596, 0.77880476030920043, 0.77478019432604039, 0.81226487639468858, 0.79991016817597915, 0.78152187831315434], [0.7095854334650713, 0.64440698454937573, 0.65604884902247496, 0.67370619285950739, 0.64949003638121472, 0.68473687310524189, 0.71775169902310654, 0.68554063651480968, 0.67559993136263852, 0.73493065087673537]]} 
vb_average_performances = {'R^2': [0.99916432522823229, 0.9882275902754788, 0.94343297364100831, 0.88925613352387933, 0.81875176139343586, 0.61794468162360316, 0.46446746734645783], 'MSE': [0.50132080190843487, 6.8543385244694743, 33.340370305040715, 66.047111100212035, 126.74049791061819, 319.57972012867043, 602.72059453333918], 'Rp': [0.99958333038463698, 0.99411536727065763, 0.97205497659988305, 0.94509347522073561, 0.90784945633265668, 0.79039179148134286, 0.68317972871601751]}

# Gibbs NMTF
gibbs_all_performances = {'R^2': [[0.9999762051562596, 0.9999803399582806, 0.9999777589782466, 0.9999709683708068, 0.999978340629859, 0.9999852791454913, 0.9999780394376246, 0.9999780429119534, 0.9999809961629468, 0.9999761694513424], [0.9892731322950635, 0.9882854518233279, 0.9900063397701583, 0.9881239121668208, 0.9869770339990847, 0.9868975318598722, 0.9866051781655802, 0.9883115546912089, 0.9861865655688425, 0.9874666234275644], [0.9438952141317052, 0.9490986446107796, 0.9501474627078781, 0.9491475620212295, 0.946260085022051, 0.9445842470668413, 0.9428754789613143, 0.9441871319960652, 0.9561083936916753, 0.9399280922411841], [0.9034148772718399, 0.8610744113070802, 0.8879519872745595, 0.916425067644823, 0.9012842171539925, 0.9085575829562682, 0.9244983175454888, 0.8817365399073894, 0.9027911239718345, 0.9129670130408155], [0.7952883145845983, 0.8427627550119179, 0.8429012794541995, 0.7670370800835049, 0.7966206655974436, 0.8306180239099952, 0.8340723236334684, 0.793407942386595, 0.7929029092002904, 0.7633524795396956], [0.597888005052394, 0.6523041696908087, 0.6246973351444023, 0.6301927676172854, 0.637402901709756, 0.6957618471471142, 0.5989932585319715, 0.6286019864387988, 0.6084617880901084, 0.6442493328175058], [0.5048388686215449, 0.47643185345917827, 0.4790398469198044, 0.4505495904416955, 0.4314043896214116, 0.3931817106175245, 0.44481216051759753, 0.47914691175030166, 0.46295347767631867, 0.474770295656618]], 'MSE': [[0.012415082985115884, 0.012306805625041068, 0.012594610111962844, 0.013270684282550224, 0.010150643671264699, 0.0089559724419040546, 0.011728490766570924, 0.0090774206002179562, 0.010051131432807723, 0.014910134987471551], [6.3650250745827917, 6.9772875134660861, 6.4605202277868203, 6.1019213235183258, 7.0274634574243411, 7.0954735436180609, 6.5175028912503032, 6.2272219239073845, 6.8898068310467746, 6.3638177906839566], [32.010298177202706, 31.487229736120653, 31.810889451524059, 29.4242904020069, 34.728693798067908, 31.382982888168932, 34.257787907612325, 32.870050586180923, 30.819384758479522, 32.034305900309292], [63.323310633723601, 70.602058737926995, 69.871820360918065, 58.881884141925894, 64.522029966843533, 64.295549232528842, 64.351886498402834, 67.461727785972201, 66.40112989798331, 60.956783887618329], [126.81416740422681, 124.84229909106757, 123.80205590433334, 129.82465610596631, 132.71500841111327, 110.11622066240963, 116.89359328338013, 123.38412528357388, 133.61574981677359, 140.56154375898188], [308.0042624208412, 303.14321326828451, 318.19342650156244, 344.97547455267596, 320.97018624061127, 307.78326016347887, 327.29382926466985, 312.31221570395195, 348.79997809616282, 303.38845949964548], [639.80911648498068, 613.5268157024218, 635.18753176310156, 597.53728342734826, 691.7763863344012, 647.7311836214451, 599.21570883873733, 644.31787764090848, 609.82917212056236, 645.68868289391617]], 'Rp': [[0.9999881065064895, 0.99999018976224585, 0.99998889239916855, 0.99998568201202054, 0.99998928827804212, 0.99999267942269332, 0.99998903099637304, 0.99998903434209263, 0.99999054909869278, 0.9999880975944504], [0.99464635578861182, 0.99415342613242608, 0.99499239381636762, 0.99405595121104184, 0.99349787233547615, 0.99348160995262647, 0.99329451353996534, 0.9941402292360294, 0.99308142207777561, 0.99373620072851132], [0.97155598274842569, 0.97422744642650227, 0.97485608013488723, 0.97438157263830005, 0.97286250234284333, 0.97193572830412578, 0.97104801932531637, 0.97176713448853169, 0.97783680372231296, 0.96957420980464581], [0.95049426165455497, 0.92830438835740114, 0.94245298491190888, 0.95767448217920093, 0.9494996725421323, 0.95319253944940974, 0.96168209553503103, 0.93905773936876447, 0.95018044859905504, 0.95553520025928307], [0.89213853598626336, 0.91812677938857157, 0.91838975360842035, 0.87653604836900689, 0.89261128945734858, 0.91145394453087225, 0.91377937423229649, 0.89086314002809908, 0.89080416524785622, 0.87384780856985478], [0.77434874913939045, 0.80848453327017944, 0.79128052617029188, 0.79425404964433588, 0.79896751623073836, 0.83422677141147528, 0.77504876533327804, 0.79346132555892146, 0.78069046405720699, 0.8032911117724455], [0.71077968104535472, 0.69118837173023373, 0.69496582313995658, 0.67132582711765865, 0.65975838457075742, 0.63169509349471398, 0.66834413469997389, 0.69282403369600454, 0.68178490055736751, 0.69099890406702391]]} 
gibbs_average_performances = {'R^2': [0.99997821402028109, 0.98781333237675251, 0.94662323124507231, 0.90007011380740898, 0.80589637734017094, 0.6318553392240146, 0.45971291052819946], 'MSE': [0.011546097690490694, 6.6026040577284846, 32.082591360567321, 65.066818114384361, 126.25694197218263, 319.48643057118841, 632.46197588278233], 'Rp': [0.99998915504122665, 0.99390799748188319, 0.97300454799358926, 0.94880738128567399, 0.89785508394185887, 0.79540538125882621, 0.67936651541190451]}


# Assemble the average performances and method names
methods = ['VB-NMTF','G-NMTF']
avr_performances = [
    vb_average_performances,
    gibbs_average_performances
]

for metric in metrics:
    plt.figure()
    #plt.title("Performances (%s) for different noise levels" % metric)
    plt.xlabel("Noise to signal ratio", fontsize=16)
    plt.ylabel(metric, fontsize=16)
    
    x = noise_ratios
    for method, avr_performance in zip(methods,avr_performances):
        y = avr_performance[metric]
        #plt.plot(x,y,label=method)
        plt.plot(x,y,linestyle='-', marker='o', label=method)
    plt.legend(loc=0)  