function parseCategory(questionLines, startLine, question) {
	question['category'] = '';
	for (let n = startLine; n < questionLines.length; n++) {
		const cline = questionLines[n];
		if (question['category'] == '') {
			question['category'] = cline;
		} else {
			question['category'] = question['category'] + '\n' + cline;
		}
	}
	question['category'] = question['category'].trimEnd();
}

function parseOptions(questionLines, startLine, question) {
	question['options'] = {};
	for (let n = startLine; n < questionLines.length; n++) {
		const cline = questionLines[n];
		if (cline === "Category:") {
			parseCategory(questionLines, n + 1, question);
			break;
		} else if (cline.startsWith("(A)")) {
			question['options']['A'] = cline;
		} else if (cline.startsWith("(B)")) {
			question['options']['B'] = cline;
		} else if (cline.startsWith("(C)")) {
			question['options']['C'] = cline;
		} else if (cline.startsWith("(D)")) {
			question['options']['D'] = cline;
		} else if ('D' in question['options']) {
			question['options']['D'] = question['options']['D'] + cline;
		} else if ('C' in question['options']) {
			question['options']['C'] = question['options']['C'] + cline;
		} else if ('B' in question['options']) {
			question['options']['B'] = question['options']['B'] + cline;
		} else if ('A' in question['options']) {
			question['options']['A'] = question['options']['A'] + cline;
		}
	}
	question['options']['A'] = question['options']['A'].trimEnd();
	question['options']['B'] = question['options']['B'].trimEnd();
	question['options']['C'] = question['options']['C'].trimEnd();
	question['options']['D'] = question['options']['D'].trimEnd();
}

function parseQuestion(questionLines) {
	let question = {}
	question['question'] = '';
	let n = 0;
	for (let n = 0; n < questionLines.length; n++) {
		const cline = questionLines[n];
		if (cline === "Options:") {
			parseOptions(questionLines, n + 1, question);
			break;
		} else if (cline === "Category:") {
			parseCategory(questionLines, n + 1, question);
			break;
		} else {
			if (question['question'] == '') {
				question['question'] = cline;
			} else {
				question['question'] = question['question'] + '\n' + cline;
			}
		}
	}
	question['question'] = question['question'].trimEnd();
	return question;
}

function parseQuestionsTxt(questionText) {
	let questionsList = [];
	let qcnt = 0;
	const qLines = questionText.split(/\r?\n|\r|\n/g);
	let questionLines = []
	for (let n = 0; n < qLines.length; n++) {
		const cline = qLines[n];
		if (cline === "Question:") {
			if (qcnt > 0) {
				questionsList.push(parseQuestion(questionLines));
				questionLines = []
			}
			qcnt++;
		} else {
			questionLines.push(cline);
		}
	}
	questionsList.push(parseQuestion(questionLines));
	return questionsList;
}

function parseQuestions(tag) {
	return parseQuestionsTxt(getQuestionsTxt(tag));
}

function parseCatQuestions(cat) {
	let questionsList = [];
	for (let key in qPaperDict){
		let keyQuestions = parseQuestionsTxt(qPaperDict[key]);
		for (let n = 0; n < keyQuestions.length; n++) {
			if ('category' in keyQuestions[n] && keyQuestions[n]['category'] == cat) {
				questionsList.push(keyQuestions[n]);
			}
		}
	}
	return questionsList;
}

var qPaperDict = {
	'2007':qp_2007,
	'2008':qp_2008,
	'2009':qp_2009,
	'2010':qp_2010,
	'2011':qp_2011,
	'2012':qp_2012,
	'2013':qp_2013,
	'2014_1':qp_2014_1,
	'2014_2':qp_2014_2,
	'2014_3':qp_2014_3,
	'2015_1':qp_2015_1,
	'2015_2':qp_2015_2,
	'2015_3':qp_2015_3,
	'2016_1':qp_2016_1,
	'2016_2':qp_2016_2,
	'2017_1':qp_2017_1,
	'2017_2':qp_2017_2,
	'2018':qp_2018,
	'2019':qp_2019,
	'2020':qp_2020,
	'2021_1':qp_2021_1,
	'2021_2':qp_2021_2,
	'2022':qp_2022,
	'2023':qp_2023
}

function getQuestionsTxt(tag) {
	return qPaperDict[tag];
}

function yearsSelectElement(){
    var selectDivTag = elementWithClassAndId('div', 'custom-select', 'yearSelect');
	selectDivTag.style = 'width:150px;';
	var selectTag = elementWithId('select', 'pyears');
    selectTag.appendChild(elementWithValueAndContent('option','0','Select Year:'));
    selectTag.appendChild(elementWithValueAndContent('option','2007','2007'));
    selectTag.appendChild(elementWithValueAndContent('option','2008','2008'));
    selectTag.appendChild(elementWithValueAndContent('option','2009','2009'));
    selectTag.appendChild(elementWithValueAndContent('option','2010','2010'));
    selectTag.appendChild(elementWithValueAndContent('option','2011','2011'));
    selectTag.appendChild(elementWithValueAndContent('option','2012','2012'));
    selectTag.appendChild(elementWithValueAndContent('option','2013','2013'));
    selectTag.appendChild(elementWithValueAndContent('option','2014_1','2014_1'));
    selectTag.appendChild(elementWithValueAndContent('option','2014_2','2014_2'));
    selectTag.appendChild(elementWithValueAndContent('option','2014_3','2014_3'));
    selectTag.appendChild(elementWithValueAndContent('option','2015_1','2015_1'));
    selectTag.appendChild(elementWithValueAndContent('option','2015_2','2015_2'));
    selectTag.appendChild(elementWithValueAndContent('option','2015_3','2015_3'));
    selectTag.appendChild(elementWithValueAndContent('option','2016_1','2016_1'));
    selectTag.appendChild(elementWithValueAndContent('option','2016_2','2016_2'));
	selectTag.appendChild(elementWithValueAndContent('option','2017_1','2017_1'));
    selectTag.appendChild(elementWithValueAndContent('option','2017_2','2017_2'));
    selectTag.appendChild(elementWithValueAndContent('option','2018','2018'));
    selectTag.appendChild(elementWithValueAndContent('option','2019','2019'));
    selectTag.appendChild(elementWithValueAndContent('option','2020','2020'));
	selectTag.appendChild(elementWithValueAndContent('option','2021_1','2021_1'));
    selectTag.appendChild(elementWithValueAndContent('option','2021_2','2021_2'));
    selectTag.appendChild(elementWithValueAndContent('option','2022','2022'));
    selectTag.appendChild(elementWithValueAndContent('option','2023','2023'));
	selectDivTag.appendChild(selectTag);
    return selectDivTag;
}

