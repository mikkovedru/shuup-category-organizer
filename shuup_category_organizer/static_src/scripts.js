/**
 * This file is part of Shuup.
 *
 * Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
 *
 * This source code is licensed under the OSL-3.0 license found in the
 * LICENSE file in the root directory of this source tree.
 */
import debounce from "lodash.debounce";

function parseChildren(children) {
    var nodes = []
    if (!children) {
        return nodes;
    }
    for (var x = 0; x < children.length; x += 1) {
        if (children[x].items) {
            for (var y = 0; y < children[x].items.length; y += 1) {
                nodes.push(parseNode(children[x].items[y]));
            }
        }
    }
    return nodes;
}

function parseNode(node) {
    return {
        id: node.id,
        position: node.position,
        visible_in_menu: node.visible_in_menu,
        children: parseChildren(node.children)
    };
}

function detachEvents() {
    // this prevents leak
    $(".category-list").off();
    $(".btn-show").off();
    $(".btn-hide").off();
    $(".btn-edit").off();
    $(".btn-duplicate").off();
}

function updateList(data) {
    detachEvents();
    $("#main-category-list").replaceWith(data);
    setup();
}

const duplicateCategory = (url, callback = null) => {
    $.ajax({
        method: "POST",
        url,
        data: {
            csrfmiddlewaretoken: window.ShuupAdminConfig.csrf
        },
        success(data) {
            detachEvents();
            $("#main-category-list").replaceWith(data);
            setup();
            if (callback) {
                callback();
            }
        }
    });
};

const saveCategories = (updateList = false, callback = null) => {
    $.ajax({
        method: "POST",
        url: "",
        data: {
            payload: getPayload(),
            csrfmiddlewaretoken: window.ShuupAdminConfig.csrf
        },
        success(data) {
            if (updateList) {
                detachEvents();
                $("#main-category-list").replaceWith(data);
                setup();
            }
            if (callback) {
                callback();
            }
        }
    });
};
const saveCategoriesDebounced = debounce(saveCategories, 5000);

function setup() {
    const sortable = window.html5sortable(".category-list", {
        forcePlaceholderSize: true,
        placeholderClass: "placeholder",
        items: ".category-item",
        acceptFrom: ".category-list",
        placeholder: '<div class="placeholder"></div>',
        containerSerializer() {
            return null;
        },
        itemSerializer(serializedItem) {
            var childrenList = $(serializedItem.node).children(".category-list");
            var serializedChildren = [];
            for (var ix = 0; ix < childrenList.length; ix += 1) {
                var serialized = window.html5sortable(childrenList[ix], "serialize");
                if (serialized && serialized.length && serialized[0].items.length) {
                    serializedChildren.push(serialized[0]);
                }
            }
            var node = $(serializedItem.node);
            return {
                id: node.data("id"),
                visible_in_menu: node.data("visible-in-menu"),
                position: serializedItem.index + 1,
                children: serializedChildren
            }
        }
    });
    $(sortable).on("sortupdate", (e) => {
        saveCategoriesDebounced();
    });
    $(sortable).on("sortstart", function (evt) {
        $("#main-category-list").addClass("dragging");
    });
    $(sortable).on("sortstop", function (evt) {
        $(".category-list").removeClass("dragging");

        $(".category-list").each(function(indexc, el) {
            if (!$(el).children().length) {
                $(el).empty();
            }
        });
    });
    $(".btn-show").click(function (evt) {
        evt.preventDefault();
        $(this).closest(".category-item").attr("data-visible-in-menu", "1");
        $(this).siblings(".btn-hide").removeClass("d-none");
        $(this).addClass("d-none");
        saveCategoriesDebounced();
    });
    $(".btn-hide").click(function (evt) {
        evt.preventDefault();
        $(this).closest(".category-item").attr("data-visible-in-menu", "0");
        $(this).siblings(".btn-show").removeClass("d-none");
        $(this).addClass("d-none");
        saveCategoriesDebounced();
    });
    $(".btn-edit").click(function (evt) {
        evt.preventDefault();
        const editUrl = $(this).closest(".category-item").data("edit-url");
        window.createQuickAddIframe(editUrl + "?mode=iframe&quick_add_callback=categoryChanged");
    });
    $(".btn-duplicate").click(function (evt) {
        evt.preventDefault();
        const duplicateUrl = $(this).closest(".category-item").data("duplicate-url");
        addLoader();
        saveCategories(false, () => {
            duplicateCategory(duplicateUrl, () => {
                $("#loader").remove();
            })
        });
    });
}

function getPayload() {
    const rootNodes = [];
    const serialized = window.html5sortable('#main-category-list', 'serialize')[0];
    for (let ix = 0; ix < serialized.items.length; ix += 1) {
        rootNodes.push(parseNode(serialized.items[ix]));
    }
    return JSON.stringify(rootNodes);
}

function addLoader() {
    const loader = document.createElement("div");
    loader.className = "loader";
    loader.id = "loader";

    const icon = document.createElement("i");
    icon.className = "fa fa-spin fa-spinner fa-3x";

    loader.appendChild(icon);
    document.body.appendChild(loader);
}

window.categoryCreated = (id, name) => {
    addLoader();
    window.closeQuickIFrame();
    saveCategories(true, () => {
        $("#loader").remove();
    });
}

window.categoryChanged = (id, name) => {
    addLoader();
    window.closeQuickIFrame();
    saveCategories(true, () => {
        $("#loader").remove();
    });
}

window.createNewCategory = () => {
    window.createQuickAddIframe(window.quickAddCategoryUrl + "?mode=iframe&quick_add_callback=categoryCreated");
}

window.saveCategories = function () {
    addLoader();
    saveCategories(true, () => {
        $("#loader").remove();
        Messages.enqueue({ tags: "success", text: gettext("Categories saved") });
    });
};

$(function() {
    setup();
});
