addTags();
var qTxt = document.getElementById('questionsContent');
qTxt.value = "";
var previewQuestionsView = true;
var previewPdfView = true;

async function saveAsFile() {
	var blob = new Blob([qTxt.value], {
		"type": "application/text"
	});
	const opts = {
		suggestedName: qFileName,
	};
	const handle = await showSaveFilePicker(opts);
	const writable = await handle.createWritable();
	await writable.write(blob);
	writable.close();
}

function question(qText) {
	const qLines = qText.split(/\r?\n|\r|\n/g);
	let line = '';
	let pline = '';
	let options = false;
	if (qLines[0] !== "Question:") {
		line = 'Question:\n'
	}
	for (let n = 0; n < qLines.length; n++) {
		const cline = qLines[n];
		if (cline.startsWith('(A)') && pline !== "Options:") {
			line = line + 'Options:\n';
			options = true;
		} else if (cline == "Options:") {
			options = true;
		}
		if (options) {
			let rline = cline;
			if (cline.startsWith('(A)')) {
				rline = rline.replace('(B)', '\n(B)');
			}
			if (cline.startsWith('(A)') || cline.startsWith('(B)')) {
				rline = rline.replace('(C)', '\n(C)');
			}
			if (cline.startsWith('(A)') || cline.startsWith('(B)') || cline.startsWith('(C)')) {
				rline = rline.replace('(D)', '\n(D)');
			}
			line = line + rline + '\n';
		} else {
			line = line + cline + '\n';
		}
		pline = cline;
	}
	return line;
}

function showPdfPreview() {
	if (previewPdfView) {
		let pyear = document.getElementById("pyears").value;
		document.getElementById('pdfContent').src = "pdf/pd_" + pyear + ".pdf";
	}
}

function createPdfPreview() {
	var iframe = document.createElement('iframe');
	let pyear = document.getElementById("pyears").value;
	if (pyear) {
		iframe.src = "pdf/pd_" + pyear + ".pdf";
	}
	iframe.id = 'pdfContent';
	iframe.className = 'pdfContent';
	iframe.frameborder = '0';
	document.getElementById("pdfPreview").appendChild(iframe);
}

function removePdfPreview() {
	const pdfPreviewContainer = document.getElementById("pdfPreview");
	while (pdfPreviewContainer.firstChild) {
		pdfPreviewContainer.removeChild(pdfPreviewContainer.lastChild);
	}
}

function pyearchange1() {
	let pyear = document.getElementById("pyears").value;
	let pYearFile = new XMLHttpRequest();
	pYearFile.open("GET", "qp/qp_" + pyear + ".txt", true);
	pYearFile.send();
	pYearFile.onreadystatechange = function () {
		if (pYearFile.readyState == 4 && pYearFile.status == 200) {
			document.getElementById('questionsContent').value = pYearFile.responseText;
			if (previewQuestionsView) {
				previewQuestions();
			}
			if (previewPdfView) {
				showPdfPreview();
			}
		}
	}
}

function pyearchange() {
	let pyear = document.getElementById("pyears").value;
	document.getElementById('questionsContent').value = getQuestionsTxt(pyear);
	if (previewQuestionsView) {
		previewQuestions();
	}
	if (previewPdfView) {
		showPdfPreview();
	}
}

function optionElement(qOption) {
    let qOptionEle = divElement('option');
    let qOptionPreEle = document.createElement('pre');
    qOptionPreEle.innerHTML = qOption;
    qOptionEle.appendChild(qOptionPreEle);
    return qOptionEle;
}

function previewQuestions() {
	if (previewQuestionsView) {
		let questions = parseQuestionsTxt(qTxt.value);
		removeChilds("questionsPreviewContainer");
		let questionsSection = document.getElementById('questionsPreviewContainer');
		for (let n = 0; n < questions.length; n++) {
			let qEle = divElement('questionContainer');
			let qnum = n + 1;
			qEle.id = "qs_" + qnum;
			let qHeadingEle = divElement('questionHeading');
			qHeadingEle.innerHTML = "Question : " + qnum;
			qEle.appendChild(qHeadingEle);
			let qContentEle = divElement('questionContent');
			let qContentPreEle = document.createElement('pre');
			qContentPreEle.innerHTML = questions[n]['question'];
			qContentEle.appendChild(qContentPreEle);
			qEle.appendChild(qContentEle);
			if ('options' in questions[n]) {
				let qOptionsEle = divElement('options');
				qOptionsEle.appendChild(optionElement(questions[n]['options']['A']));
				qOptionsEle.appendChild(optionElement(questions[n]['options']['B']));
				qOptionsEle.appendChild(optionElement(questions[n]['options']['C']));
				qOptionsEle.appendChild(optionElement(questions[n]['options']['D']));
				qEle.appendChild(qOptionsEle);
			}
			questionsSection.appendChild(qEle);
		}
	}
}

function previewQuestionsAction() {
	const previewQuestionsActionE = document.getElementById("previewQuestionsB");
	if (previewQuestionsView) {
		previewQuestionsView = false;
		removeChilds("questionsPreviewContainer");
		previewQuestionsActionE.style.background = 'grey';
	} else {
		previewQuestions();
		var r = document.querySelector(':root');
		var rs = getComputedStyle(r);
		previewQuestionsActionE.style.background = rs.getPropertyValue('--brand-color');
		previewQuestionsView = true;
	}
	changeArea();
}

function previewPdfAction() {
	const previewPdfActionE = document.getElementById("previewPdfB");
	if (previewPdfView) {
		previewPdfView = false;
		removePdfPreview();
		previewPdfActionE.style.background = 'grey';
	} else {
		createPdfPreview();
		var r = document.querySelector(':root');
		var rs = getComputedStyle(r);
		previewPdfActionE.style.background = rs.getPropertyValue('--brand-color');
		previewPdfView = true;
	}
	changeArea();
}

function changeArea() {
	if (previewPdfView && previewQuestionsView) {
		document.getElementById("appContainer").style.gridTemplateAreas = '"appHeading appHeading" "appActions appActions" "elementsContainer questionsPreviewContainer" "questionsContent  questionsPreviewContainer" "questionsContent  pdfPreview"';
	} else if (previewPdfView) {
		document.getElementById("appContainer").style.gridTemplateAreas = '"appHeading appHeading" "appActions appActions" "elementsContainer pdfPreview" "questionsContent  pdfPreview" "questionsContent  pdfPreview"';
	} else if (previewQuestionsView) {
		document.getElementById("appContainer").style.gridTemplateAreas = '"appHeading appHeading" "appActions appActions" "elementsContainer questionsPreviewContainer" "questionsContent  questionsPreviewContainer" "questionsContent  questionsPreviewContainer"';
	} else {
		document.getElementById("appContainer").style.gridTemplateAreas = '"appHeading appHeading" "appActions appActions" "elementsContainer elementsContainer" "questionsContent  questionsContent" "questionsContent  questionsContent"';
	}
}

