// this stores the configuration files for all the benchmarks
// refer to: https://github.com/fredfeng/Morpheus/tree/master/ae-pldi17-morpheus/benchmarks
var benchmarks = {

	// ========== Morpheus1 ========== //
	"Morpheus1": {
		"size": 3,
		"enumerator": "ngram",
		"spec": "morpheus",
		"input0": [
			["round","var1","var2","nam","val"],
			["round1",22,33,"foo",0.169122009770945],
			["round2",11,44,"foo",0.185708264587447],
			["round1",22,33,"bar",0.124105813913047],
			["round2",11,44,"bar",0.0325823465827852]
		],
		"input1": null,
		"output": [
			["nam","val_round1","val_round2","var1_round1","var1_round2","var2_round1","var2_round2"],
			["bar",0.124105813913047,0.0325823465827852,22,11,33,44],
			["foo",0.169122009770945,0.185708264587447,22,11,33,44]
		],
		"title": "long to wide with dplyr",
		"question": 
`I have a data frame which is structured like this one:

\`dd <- data.frame(round = c("round1", "round2", "round1", "round2"),
                 var1 = c(22, 11, 22, 11),
                 var2 = c(33, 44, 33, 44),
                 nam = c("foo", "foo", "bar", "bar"),
                 val = runif(4))

   round var1 var2 nam        val
1 round1   22   33 foo 0.32995729
2 round2   11   44 foo 0.89215038
3 round1   22   33 bar 0.09213526
4 round2   11   44 bar 0.82644723\`
From this I would like to obtain a data frame with two lines, one for each value of \`nam\`, and variables \`var1_round1\`, \`var1_round2\`, \`var2_round1\`, \`var2_round2\`, \`val_round1\`, \`val_round2\`. I would really like to find a dplyr solution to this.

\`  nam var1_round1 var1_round2 var2_round1 var2_round2 val_round1 val_round2
1 foo          22          11          33          44 0.32995729  0.8921504
2 bar          22          11          33          44 0.09213526  0.8264472\`
The closest thing I can think of would be to use \`spread()\` in some creative way but I can't seem to figure it out.`
	},

	// ========== Morpheus2 ========== //
	"Morpheus2": {
		"size": 3,
		"enumerator": "ngram",
		"spec": "morpheus",
		"input0": [
			["month","student","A","B"],
			[1,"Amy",9,6],
			[2,"Amy",7,7],
			[3,"Amy",6,8],
			[1,"Bob",8,5],
			[2,"Bob",6,6],
			[3,"Bob",9,7]
		],
		"input1": null,
		"output": [
			["month","Amy_A","Amy_B","Bob_A","Bob_B"],
			[1,9,6,8,5],
			[2,7,7,6,6],
			[3,6,8,9,7]
		],
		"title": "R spreading multiple columns with tidyr",
		"question":
`
Take this sample variable

\`df <- data.frame(month=rep(1:3,2),
                 student=rep(c("Amy", "Bob"), each=3),
                 A=c(9, 7, 6, 8, 6, 9),
                 B=c(6, 7, 8, 5, 6, 7))\`
I can use \`spread\` from \`tidyr\` to change this to wide format.

\`> df[, -4] %>% spread(student, A)
  month Amy Bob
1     1   9   8
2     2   7   6
3     3   6   9\`
But how can I spread two values e.g. both \`A\` and \`B\`, such that the output is something like

\`  month Amy.A Bob.A Amy.B Bob.B
1     1     9     8     6     5
2     2     7     6     7     6
3     3     6     9     8     7\``
	},

	// ========== Morpheus3 ========== //
	"Morpheus3": {
		"size": 3,
		"enumerator": "ngram",
		"spec": "morpheus",
		"input0": [
			["Person","Time","Score1","Score2"],
			["greg","Pre",88,84],
			["greg","Post",78,82],
			["sally","Pre",76,72],
			["sally","Post",78,79]
		],
		"input1": null,
		"output": [
			["Person","Post_Score1","Post_Score2","Pre_Score1","Pre_Score2"],
			["greg",78,82,88,84],
			["sally",78,79,76,72]
		],
		"title": "How can I spread repeated measures of multiple variables into wide format?",
		"question":
`I'm trying to take columns that are in long format and spread them to wide format as shown below. I'd like to use tidyr to solve this with the data manipulation tools I'm investing in but to make this answer more general please provide other solutions.

Here's what I have:

\`library(dplyr); library(tidyr)

set.seed(10)
dat <- data_frame(
    Person = rep(c("greg", "sally", "sue"), each=2),
    Time = rep(c("Pre", "Post"), 3),
    Score1 = round(rnorm(6, mean = 80, sd=4), 0),
    Score2 = round(jitter(Score1, 15), 0),
    Score3 = 5 + (Score1 + Score2)/2
)

##   Person Time Score1 Score2 Score3
## 1   greg  Pre     80     78   84.0
## 2   greg Post     79     80   84.5
## 3  sally  Pre     75     74   79.5
## 4  sally Post     78     78   83.0
## 5    sue  Pre     81     78   84.5
## 6    sue Post     82     81   86.5\`
Desired wide format:

\`  Person Pre.Score1 Pre.Score2 Pre.Score3  Post.Score1 Post.Score2 Post.Score3
1   greg         80         78       84.0           79          80        84.5
2  sally         75         74       79.5           78          78        83.0
3    sue         81         78       84.5           82          81        86.5\`
I can do it by doing something like this for each score:

\`spread(dat %>% select(Person, Time, Score1), Time, Score1) %>% 
    rename(Score1_Pre = Pre, Score1_Post = Post)\`
And then using \`_join\` but that seems verbose and like there's got to be a better way.

Related questions:
tidyr wide to long with two repeated measures
Is it possible to use spread on multiple columns in tidyr similar to dcast?`
	}

}