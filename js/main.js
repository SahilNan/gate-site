function optionElement(qOption) {
    let qOptionEle = divElement('option');
    qOptionEle.appendChild(preElement(qOption));
    return qOptionEle;
}

function catchange() {
    let selectCategory = document.getElementById("selectCategory").value;
    viewQuestions(parseCatQuestions(selectCategory));
}

function viewQuestions(questions) {
    removeChilds('questionsSection');
    let questionsSection = document.getElementById('questionsSection');
    for (let n = 0; n < questions.length; n++) {
        let qEle = divElement('questionContainer');
        let qnum = n + 1;
        qEle.id = "qs_" + qnum;
        let qHeadingEle = divElement('questionHeading');
        qHeadingEle.innerHTML = "Question : " + qnum;
        qEle.appendChild(qHeadingEle);
        let qContentEle = divElement('questionContent');
        qContentEle.appendChild(preElement(questions[n]['question']));
        qEle.appendChild(qContentEle);
        if ('options' in questions[n]) {
            let qOptionsEle = divElement('options');
            qOptionsEle.appendChild(optionElement(questions[n]['options']['A']));
            qOptionsEle.appendChild(optionElement(questions[n]['options']['B']));
            qOptionsEle.appendChild(optionElement(questions[n]['options']['C']));
            qOptionsEle.appendChild(optionElement(questions[n]['options']['D']));
            qEle.appendChild(qOptionsEle);
        }
        if ('category' in questions[n]) {
            let qCatEle = divElement('category');
            qCatEle.innerHTML = questions[n]['category'];
            qEle.appendChild(qCatEle);
        }
        questionsSection.appendChild(qEle);
    }
}

function pyearchange() {
    let pyear = document.getElementById("pyears").value;
    viewQuestions(parseQuestions(pyear));
}

function categorySelectElement(){
    var selectDivTag = elementWithClassAndId('div', 'custom-select', 'catSelect');
	selectDivTag.style = 'width:200px;';
	var selectTag = elementWithId('select', 'selectCategory');
    selectTag.appendChild(elementWithValueAndContent('option','0','Filter Category:'));
    selectTag.appendChild(elementWithValueAndContent('option','GeneralAptitude','GeneralAptitude'));
    selectTag.appendChild(elementWithValueAndContent('option','EngineeringMathematics','EngineeringMathematics'));
    selectTag.appendChild(elementWithValueAndContent('option','DigitalLogic','DigitalLogic'));
    selectTag.appendChild(elementWithValueAndContent('option','ComputerOrganizationAndArchitecture','ComputerOrganizationAndArchitecture'));
    selectTag.appendChild(elementWithValueAndContent('option','Algorithms','Algorithms'));
    selectTag.appendChild(elementWithValueAndContent('option','OperatingSystem','OperatingSystem'));
    selectTag.appendChild(elementWithValueAndContent('option','Databases','Databases'));
    selectTag.appendChild(elementWithValueAndContent('option','ComputerNetworks','ComputerNetworks'));
	selectDivTag.appendChild(selectTag);
    return selectDivTag;
}

function previewQuestionsPage(){
    let headerSection = elementWithClass('section', 'header-content');
    let headerTitle = elementWithClass('div', 'header-title');
    headerTitle.appendChild(elementWithContent('span', 'Previous Year'));
    headerTitle.appendChild(elementWithContent('h2', 'Questions'));
    headerSection.appendChild(headerTitle);
    let searchContainer = elementWithClass('div', 'search-container');
    let inputEle = document.createElement('input');
    inputEle.type = 'text';
    inputEle.placeholder = 'Search..';
    inputEle.name = 'search';
    inputEle.style= "padding:8px";

    searchContainer.appendChild(inputEle);
    let butEle = document.createElement('button');
    butEle.type = 'submit';
    //butEle.appendChild(elementWithClassAndContent('span', 'material-icons', 'search'));
    searchContainer.appendChild(butEle);

    headerSection.appendChild(searchContainer);

    headerSection.appendChild(categorySelectElement());
    headerSection.appendChild(yearsSelectElement());
    document.getElementById('mainContent').appendChild(headerSection);
    document.getElementById('mainContent').appendChild(elementWithClassAndId('section','questions-section','questionsSection'));
    processSelect("catSelect",catchange);
    processSelect("yearSelect",pyearchange);
}

function editQuestionsPage(){
    let headerSection = elementWithClass('section', 'header-content');
    let headerTitle = elementWithClass('div', 'header-title');
    headerTitle.appendChild(elementWithContent('span', 'Previous Year'));
    headerTitle.appendChild(elementWithContent('h2', 'Questions'));
    headerSection.appendChild(headerTitle);
    headerSection.appendChild(yearsSelectElement());
    document.getElementById('mainContent').appendChild(headerSection);
    document.getElementById('mainContent').appendChild(elementsContainer());
    document.getElementById('mainContent').appendChild(elementWithClassAndId('section','questions-section','questionsSection'));
    processSelect("yearSelect",pyearchange);
}