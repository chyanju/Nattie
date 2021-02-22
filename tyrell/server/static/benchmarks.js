// this stores the configuration files for all the benchmarks
var benchmarks = {

	"MorpheusP2": {
		"size": 3,
		"enumerator": "ngram",
		"spec": "morpheus",
		"input0": [
			["date","ship","latt","long"],
			["1-1-2018","Baltimore",41.3,61.4],
			["2-1-2018","Baltimore",7.1,17.5],
			["3-1-2018","Baltimore",6.3,81.4],
			["1-1-2018","Chester",82.1,52.3],
			["2-1-2018","Chester",6.3,62.1],
			["3-1-2018","Chester",9.9,73.2]
		],
		"input1": null,
		"output": [
			["date","Baltimore_latt","Baltimore_long","Chester_latt","Chester_long"],
			["1-1-2018",41.3,61.4,82.1,52.3],
			["2-1-2018",7.1,17.5,6.3,62.1],
			["3-1-2018",6.3,81.4,9.9,73.2]
		]
	},

	"MorpheusP3": {
		"size": 3,
		"enumerator": "ngram",
		"spec": "morpheus",
		"input0": [
			["Person","Time","Score1","Score2"],
			["greg","Pre",75,76],
			["greg","Post",86,85],
			["sally","Pre",85,86],
			["sally","Post",80,78]
		],
		"input1": null,
		"output": [
			["Person","Post_Score1","Post_Score2","Pre_Score1","Pre_Score2"],
			["greg",86,85,75,76],
			["sally",80,78,85,86]
		]
	}

}