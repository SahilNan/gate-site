function divElement(className) {
	var div = document.createElement("div");
	div.setAttribute("class", className);
	return div;
}

function aElement(refUrl) {
	var aEle = document.createElement("a");
	aEle.setAttribute("href", refUrl);
	return aEle;
}

function elementWithClassAndContent(tagName, className, content) {
	let tagEle = document.createElement(tagName);
	tagEle.setAttribute("class", className);
	tagEle.innerHTML = content;
	return tagEle;
}

function elementWithClassAndId(tagName, className, id) {
	let tagEle = document.createElement(tagName);
	tagEle.setAttribute("class", className);
	tagEle.id = id;
	return tagEle;
}

function elementWithId(tagName, id) {
	let tagEle = document.createElement(tagName);
	tagEle.id = id;
	return tagEle;
}

function elementWithClass(tagName, className) {
	let tagEle = document.createElement(tagName);
	tagEle.setAttribute("class", className);
	return tagEle;
}

function elementWithValueAndContent(tagName, value, content) {
	let tagEle = document.createElement(tagName);
	tagEle.value = value;
	tagEle.innerHTML = content;
	return tagEle;
}

function elementWithContent(tagName, content) {
	let tagEle = document.createElement(tagName);
	tagEle.innerHTML = content;
	return tagEle;
}

function tagElementWithContent(tagName, content) {
	let tagEle = document.createElement(tagName);
	tagEle.innerHTML = content;
	return tagEle;
}

function spanElement(content) {
	return tagElementWithContent('span', content);
}

function removeChilds(id) {
	const questionsPreviewContainer = document.getElementById(id);
	while (questionsPreviewContainer.firstChild) {
		questionsPreviewContainer.removeChild(questionsPreviewContainer.lastChild);
	}
}

function processClassElements(className, processFunction) {
	let selectItems = document.getElementsByClassName(className);
	let selectItemsLen = selectItems.length;
	for (let i = 0; i < selectItemsLen; i++) {
		processFunction(i, selectItems[i]);
	}
}

function preElement(content) {
	return tagElementWithContent('pre', content);
}

function closeAllSelect(elmnt) {
	let arrNo = [];
	processClassElements("select-selected", function (idx, selElem) {
		if (elmnt == selElem) {
			arrNo.push(idx)
		} else {
			selElem.classList.remove("select-arrow-active");
		}
	});
	processClassElements("select-items", function (idx, selElem) {
		if (arrNo.indexOf(idx)) {
			selElem.classList.add("select-hide");
		}
	});
}

function addSelectClickEvent(elmnt) {
	elmnt.addEventListener("click", function (e) {
		e.stopPropagation();
		closeAllSelect(this);
		this.nextSibling.classList.toggle("select-hide");
		this.classList.toggle("select-arrow-active");
	});
}

function removeClass(elmts) {
	let elmtsLen = elmts.length;
	for (k = 0; k < elmtsLen; k++) {
		elmts[k].removeAttribute("class");
	}
}

function processSelect(selectId, selectFunction) {
	var a, b, c;
	var yearSelect = document.getElementById(selectId);
	let selElmnt = yearSelect.getElementsByTagName("select")[0];
	a = divElement("select-selected");
	a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
	yearSelect.appendChild(a);
	b = divElement("select-items select-hide");
	let selElmntLen = selElmnt.length;
	for (let j = 1; j < selElmntLen; j++) {
		c = document.createElement("div");
		c.innerHTML = selElmnt.options[j].innerHTML;
		c.addEventListener("click", function (e) {
			var s, h;
			s = this.parentNode.parentNode.getElementsByTagName("select")[0];
			h = this.parentNode.previousSibling;
			let sl = s.length;
			for (let i = 0; i < sl; i++) {
				if (s.options[i].innerHTML == this.innerHTML) {
					s.selectedIndex = i;
					h.innerHTML = this.innerHTML;
					removeClass(this.parentNode.getElementsByClassName("same-as-selected"));
					this.setAttribute("class", "same-as-selected");
					break;
				}
			}
			h.click();
			selectFunction();
		});
		b.appendChild(c);
	}
	yearSelect.appendChild(b);
	addSelectClickEvent(a);
}