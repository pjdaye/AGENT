function isElementOrParentOfElement(left, right) {
    var attempt = left == right;

    if (!attempt && $(right).children().length > 0) {
        attempt = left == $(right).children()[0];
    }

    if (!attempt && $(left).siblings().length > 0) {
        attempt = $(left).siblings()[0] == right;
    }

    return attempt;
}

function isElementClickable(element) {
    var output = false;

    var origScroll = $(window).scrollTop();

    element = $(element)[0];

    if (element.scrollIntoView) {
        element.scrollIntoView(false);
    } else {
        var old_position = calculate_position(element);
        $(window).scrollTop(old_position.y);
    }

    var position = calculate_position(element);

    var jq_position = null;

    try {
        jq_position = $(element).position();
    } catch (ex) {}

    if (
        isElementOrParentOfElement(
            document.elementFromPoint(
                position.x + position.width / 2,
                position.yRelative
            ),
            element
        )
    ) {
        output = true;
    }

    if (
        !output &&
        isElementOrParentOfElement(
            document.elementFromPoint(position.x, position.yRelative),
            element
        )
    ) {
        output = true;
    }

    if (
        !output &&
        isElementOrParentOfElement(
            document.elementFromPoint(position.x + 15, position.yRelative + 20),
            element
        )
    ) {
        output = true;
    }

    if (
        !output &&
        isElementOrParentOfElement(
            document.elementFromPoint(
                position.x + position.width / 2,
                position.yRelative + 10
            ),
            element
        )
    ) {
        output = true;
    }

    if (
        !output &&
        isElementOrParentOfElement(
            document.elementFromPoint(jq_position.left, position.yRelative),
            element
        )
    ) {
        output = true;
    }

    if (!output && jq_position) {
        output = isElementOrParentOfElement(
            document.elementFromPoint(
                jq_position.left + position.width / 2,
                position.yRelative
            ),
            element
        );
        output =
            output ||
            isElementOrParentOfElement(
                document.elementFromPoint(
                    jq_position.left + position.width / 2,
                    position.yRelative
                ),
                element
            );
    }

    $(window).scrollTop(origScroll);

    return output;
}

function makeUniqueID(element, properties) {
    var id = "";

    id += element.prop("tagName") || "text";

    id = id + (element.prop("id") || "");

    id = id + calculateIndexValue(element);
    id = id + ":" + element.parents().length;

    return id;
}

function calculateIndexValue(element) {
    if (element.parent().length === 0) return "0";

    parent_index = calculateIndexValue(element.parent());
    index = parent_index + "_" + element.index();
    return index;
}

function isVirtualTextNode(element) {
    try {
        return (
            element.contents().length === 1 &&
            element.contents()[0].nodeType === 3
        );
    } catch (ex) {
        return false;
    }
}

function origin_position() {
    position = {
        x: 0,
        y: 0,
        width: 0,
        height: 0,
        yRelative: 0
    };
    return position;
}

function calculate_rect_position(element_node) {
    var position = null;

    try {
        var bodyRect = document.body.getBoundingClientRect();
        var elemRect = element_node.getBoundingClientRect();
        var topOffset = elemRect.top - bodyRect.top;
        var leftOffset = elemRect.left - bodyRect.left;

        position = origin_position();
        position.width = elemRect.width;
        position.height = elemRect.height;
        position.x = leftOffset;
        position.y = topOffset;
        position.yRelative = elemRect.top;
    } catch (ex) {
        var bodyRect = document.body.getBoundingClientRect();
        var range = document.createRange();
        var rect = {};
        var domElement = {
            name: "",
            domLevel: 0,
            identifier: "",
            properties: {},
            actions: [],
            children: []
        };

        range.selectNodeContents(element_node);

        var elemRect = range.getBoundingClientRect();

        var topOffset = elemRect.top - bodyRect.top;
        var leftOffset = elemRect.left - bodyRect.left;

        position = origin_position();
        position.width = elemRect.width;
        position.height = elemRect.height;
        position.x = leftOffset;
        position.y = topOffset;
        position.yRelative = elemRect.top;
    }
    return position;
}

function calculate_position(element_node) {
    position = origin_position();
    element = $(element_node);

    var tag = element.prop("tagName");
    if (tag) {
        tag = tag.toLowerCase();
    }

    if (!tag) {
        position = calculate_rect_position(element_node);
    } else if (tag === "html" || tag === "body") {
        position.x = element.prop("offsetLeft");
        position.y = element.prop("offsetTop");
        position.width = element.width();
        position.height = element.height();
    } else {
        var clientWidth = element.prop("clientWidth");
        var clientHeight = element.prop("clientHeight");

        position = calculate_rect_position(element_node);
        if (!position) {
            position = origin_position();
            position.width = element.width();
            position.height = element.height();
            position.x = element.prop("offsetLeft");
            position.y = element.prop("offsetTop");
            position.yRelative = position.y;
        }
    }

    var offset = 0;
    if (tag === "input") {
        position.y -= offset;
    } else {
        position.y -= offset;
    }
    return position;
}

function makeBaseElement(element, position, tagName) {
    var domElement = {
        name: "",
        domLevel: 0,
        identifier: "",
        properties: {},
        actions: [],
        children: []
    };

    domElement.domLevel = element.parents().length;
    domElement.identifier = element.prop("id");
    if (element.prop("name")) {
        domElement.name = element.prop("name");
    }

    var domAttributes = domElement.properties;
    domAttributes["tagName"] = tagName;
    domAttributes["x"] = position.x;
    domAttributes["y"] = position.y;
    domAttributes["xPercent"] = position.x / $(document).width() * 100.0;
    domAttributes["yPercent"] = position.y / $(document).height() * 100.0;
    domAttributes["height"] = position.height;
    domAttributes["width"] = position.width;
    domAttributes["value"] = element.val();

    var tag = tagName.toLowerCase();

    if (tag == "select") {
        domAttributes["value"] = element.find("option:selected").text();
    }

    domAttributes["type"] = element.attr("type") || "";

    try {
        var style = window
            .getComputedStyle(element[0], null)
            .getPropertyValue("font-size");
        var fontSize = parseFloat(style);

        domAttributes["fontSize"] = fontSize;

        domAttributes["class"] = element.attr("class");
    } catch (ex) {}

    return domElement;
}

function makeDOMElement(element_node) {
    var element = $(element_node);
    var position = calculate_position(element_node);

    var tagName = element.prop("tagName");
    var tag = tagName.toLowerCase();
    var domElement = makeBaseElement(element, position, tagName);
    var domAttributes = domElement.properties;

    domAttributes["is-hidden"] = !isElementClickable(element);
    domAttributes["is-focused"] = $(element).is(":focus");
    domAttributes["font-family"] = element.css("font-family");
    domAttributes["background-color"] = element.css("background-color");
    domAttributes["color"] = element.css("color");
    domAttributes["font-weight"] = element.css("font-weight");

    $.each(element.get(0).attributes, function(i, attrib) {
        domAttributes[attrib.name] = attrib.value;
    });

    if (tag === "input" && domAttributes["type"].toLowerCase() === "radio") {
        domAttributes["checked"] = element.attr("checked");
    }

    if (tag === "select") {
        var values = [];
        var text = [];
        $.each(element.find("option"), function(i, option) {
            var new_value = $(option).val();
            var new_value_text = $(option).text();
            values.push(new_value);
            text.push(new_value_text);
        });

        domAttributes["values"] = text;
        domAttributes["valuesText"] = text;
    }

    if (isVirtualTextNode(element)) {
        domAttributes["text"] = element.text().trim();
    } else {
        domAttributes["text"] = "";
    }

    if (tag === "button") {
        domAttributes["text"] = element.text().trim();
    }

    return domElement;
}

function makeTextElement(element_node) {
    var element = $(element_node);
    var position = calculate_position(element_node);

    domElement = makeBaseElement(element, position, "#text");
    var domAttributes = domElement.properties;

    domAttributes["is-hidden"] = false;
    domAttributes["font-family"] = element.parent().css("font-family");
    domAttributes["background-color"] = element
        .parent()
        .css("background-color");
    domAttributes["color"] = element.parent().css("color");
    domAttributes["font-weight"] = element.parent().css("font-weight");
    domAttributes["text"] = element.text().trim();
    return domElement;
}

function findValidID(data, parentID, id) {
    if (data.widgets[parentID].children[id]) {
        var index = id.split("_")[1];

        if (index) index++;
        else index = 1;

        id = id.split("_")[0] + "_" + index;

        return findValidID(data, parentID, id);
    }

    return id;
}

function addWidget(data, element_node, isText) {
    var id;
    var parentID;
    var node;
    var element = $(element_node);

    var parent = element.parent();
    var parent_node = parent["0"];
    var parentRect = {
        x: parent.position().left,
        y: parent.position().top
    };

    parentID = makeUniqueID(parent, parentRect);

    if (isText) {
        node = makeTextElement(element_node);
    } else {
        node = makeDOMElement(element_node);
    }

    id = makeUniqueID(element, node.properties);
    node.key = id;

    if (!data.widgets[parentID]) {
        var new_parent = makeDOMElement(parent_node);
        new_parent.key = parentID;
        data.widgets[parentID] = new_parent;
    }

    data.widgets[parentID].children.push(node.key);
    data.widgets[id] = $.extend(true, {}, node);

    if (parentID.startsWith("HTML")) {
        data.root = id;
    }

    data.elements[parentID] = parent;
    data.elements[id] = element;
    element.data("widget-json", id);

    return element;
}

function scrape_for_widgets(data, cur_doc, element) {
    widget_number = 0;
    element.find(":visible").each(function(i, element_node) {
        element = addWidget(data, element_node, false);

        if (!isVirtualTextNode(element)) {
            try {
                element.contents().each(function(i, text_node) {
                    if (
                        $(text_node).prop("tagName") === undefined &&
                        $(text_node)
                            .text()
                            .trim() !== ""
                    ) {
                        addWidget(data, text_node, true);
                    }
                });
            } catch (ex) {}
        }

        if (element.prop("tagName").toLowerCase() === "iframe") {
            var iframe_id = element.prop("id");
            var iframe = cur_doc.getElementById(iframe_id);
            var baseURI = iframe.baseURI;
            var src = iframe.src;

            if (!cross_site(baseURI, src)) {
                var iFrameDoc = iframe.contentWindow.document;
                var iFrameElement = $(iFrameDoc.body);
                scrape_for_widgets(data, iFrameDoc, iFrameElement);
            }
        }
    });
}

function cross_site(uri1, uri2) {
    var host1 = get_host_from_url(uri1);
    var host2 = get_host_from_url(uri2);
    if (host1 === host2) {
        return false;
    }
    return true;
}

function get_host_from_url(url) {
    var parser = document.createElement("a");
    parser.href = url;

    return parser.hostname;
}

window.aist_scrape = function() {
    var data = {
        url: "",
        title: "",
        widgets: {},
        elements: {}
    };

    data.url = window.location.href;
    data.title = document.title;

    if (!data.title || data.title === "") {
        data.title = window.location.pathname.split("/").pop();
    }

    scrape_for_widgets(data, document, $("html"));

    return data;
};