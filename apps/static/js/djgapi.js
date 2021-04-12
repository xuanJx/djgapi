var createElement = (tagName, attrs, childrens) => {
    let dom = document.createElement(tagName);
    if (attrs && Object.keys(attrs).length > 0) {
        attrsName = Object.keys(attrs);
        for (let item of attrsName) {
            let value = attrs[item];
            if (item in dom) {
                if (value.constructor === Object) {
                    Object.keys(value).forEach(valueItem=> {
                        dom[item][valueItem] = value[valueItem];
                    });
                } else if (typeof dom[item] === "string" || typeof dom[item] === "number") {
                    dom[item] = value;
                } else if (dom[item] && typeof dom[item].constructor === Array) {
                    dom[item] = value;
                } else {
                    dom.setAttribute(item, value)
                }
            } else {
                dom.setAttribute(item, value)
            }
        }
    }
    if (childrens && childrens.constructor === Array && childrens.length > 0) {
        for (let childObj of childrens) {
            if (childObj.constructor === Object && childObj.tagName) {
                let child = createElement(childObj.tagName, childObj.attrs, childObj.childrens);
                dom.appendChild(child);
            }
        }
    }
    return dom;
};

var setUrlParam = (url, name, value) => {
    let urlArray = url.split('?');
    if (urlArray.length === 1) {
        url += "?" + name + '=' + value
    } else {
        let oriParam = urlArray[1].split("&");
        let oriParamMap = {};
        for (let i of oriParam) {
            let v = i.split("=");
            oriParamMap[v[0]] = v[1];
        }
        oriParamMap[name] = value;
        url = urlArray[0] + "?";
        let newParam = [];
        for (let item of Object.keys(oriParamMap)) {
            newParam.push(item + "=" + oriParamMap[item])
        }
        url += newParam.join("&")
    }
    return url
};

var removeNavUlElement = ()=>{
    const aulId = document.getElementById('ulNav')
    while(aulId.hasChildNodes()){
        aulId.removeChild(aulId.firstChild)
    }
}

var removeAulElement = ()=>{
    const aulId = document.getElementById('aul')
    while(aulId.hasChildNodes()){
        aulId.removeChild(aulId.firstChild)
    }
}

var removeBulElement = ()=>{
    const bulId = document.getElementById('bul')
    while(bulId.hasChildNodes()){
        bulId.removeChild(bulId.firstChild)
    }
}

var inputValSet = (inputElemtent, val, elemtent, arr, value) => {
    $(inputElemtent).val(val)
    document.getElementById(elemtent).setAttribute(arr, value)
}

var eventRedirect = (element, event, url) => {
    element.addEventListener(event, function () {
        window.location.replace(url)
    })
}

