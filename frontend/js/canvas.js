var glbl = (function() {
    var n;
    var canvas;
    var padding;
    var width, height;
    var xOffset, yOffset;
    var xCellCount, yCellCount;
    var gridCount;
    var context;
    var cellSize;
    var values = [];
    var x = -1,
        y = -1;
    return {
        n: n,
        canvas: canvas,
        padding: padding,
        width: width,
        height: height,
        xOffset: xOffset,
        yOffset: yOffset,
        xCellCount: xCellCount,
        yCellCount: yCellCount,
        gridCount: gridCount,
        context: context,
        cellSize: cellSize,
        values: values,
        x: x,
        y: y,
    };
})();

var $class = function(definition) {
    var constructor = definition.constructor; 
    var parent = definition.Extends;
    if (parent) {
        var F = function() { };
        constructor._superClass = F.prototype = parent.prototype;
        constructor.prototype = new F();
    }
    for (var key in definition) {
        constructor.prototype[key] = definition[key];
    }
    constructor.prototype.constructor = constructor;
    return constructor;
};

glbl.n = 40;

/*
function getGrid(c) {
    return Math.round(c / glbl.cellSize);
}

function getRelPos(c) {
    return c - getAbsPos(getCell(c));
}

function getAbsPos(c) {
    return c * glbl.cellSize;
}

function getMiddle(a, b) {
    return Math.floor((a + b) / 2);
}

function getMaxVal() {
    return glbl.values.reduce(function(max, arr) {
        var value = arr.reduce(function(max, arr2) {
            return max >= arr2 ? max : arr2;
        }, -Infinity)
        return max >= value ? max : value;
    }, -Infinity);
}

function getMinVal() {
    return glbl.values.reduce(function(min, arr) {
        var value = arr.reduce(function(min, arr2) {
            return min <= arr2 ? min : arr2;
        }, Infinity)
        return min <= value ? min : value;
    }, Infinity);
}
*/


(function(window) {
    $(document).ready(function($) {
        initGrid();

        $('canvas').get(0).addEventListener('mousedown', function(e) {
            data = getData();
            cx = getCellX(getMouseX(e.pageX));
            cy = getCellY(getMouseY(e.pageY));
            console.log(data[cx][cy]);
            //fillCell(cx, cy, 64);
            //fillGrid(data);
        });         
    });
}(window));

function initGrid() {
    setPrivateProperties();
    drawGrid();
}

function setPrivateProperties() {
    glbl.cellSize = getCellSize();
    glbl.xCellCount = getXCellCount();
    glbl.yCellCount = getYCellCount();
    glbl.width = glbl.xCellCount * glbl.cellSize;
    glbl.height = glbl.yCellCount * glbl.cellSize;
    glbl.padding = 0;
    var cw = glbl.width + (glbl.padding*2) + 1;
    var ch = glbl.height + (glbl.padding*2) + 1;

    glbl.canvas = $('<canvas/>').attr({width: cw, height: ch}).appendTo('.container').get(0);
    glbl.context = glbl.canvas.getContext("2d");
    glbl.xOffset = getXOffset();
    glbl.yOffset = getYOffset();
}

function drawGrid() {
    glbl.context.beginPath();
    for (var x = 0; x <= glbl.height; x += glbl.cellSize) {
        glbl.context.moveTo(glbl.padding, 0.5 + x + glbl.padding);
        glbl.context.lineTo( glbl.width + glbl.padding, 0.5 + x + glbl.padding);
    }

    for (var x = 0; x <=  glbl.width; x += glbl.cellSize) {
        glbl.context.moveTo(0.5 + x + glbl.padding, glbl.padding);
        glbl.context.lineTo(0.5 + x + glbl.padding, glbl.height + glbl.padding);
    }

    glbl.context.strokeStyle = "black";
    glbl.context.stroke();
}

function fillGrid(data) {
    console.log(data);
    var i = 0, j = 0;
    for (x in data) {
        for (y in data[i]) {
            for (var k = 0; k < data[i][j].length; k += 1) {
                fillCell(i, j, data[i][j][k]);  
            }
            j += 1;
        }
        i += 1;
        j = 0;
    }
}

function fillCell(cx, cy, value) {
    var color = value * 30;
    glbl.context.fillStyle = 0;
    glbl.context.fillRect(getAbsPosX(cx), getAbsPosY(cy), glbl.cellSize - 1, glbl.cellSize - 1);
    glbl.context.fillStyle = 'rgb(' + [color, 255 - color, color].join(',') + ')';
    glbl.context.fillRect(getAbsPosX(cx), getAbsPosY(cy), glbl.cellSize - 1, glbl.cellSize - 1);
}

function getAbsPosX(c) {
    return c * glbl.cellSize + 1;
}

function getAbsPosY(c) {
    return c * glbl.cellSize + 1;
}

function getCellX(c) {
    var cell = Math.floor(c / glbl.cellSize);
    return (cell >= glbl.xCellCount) ? cell - 1 : cell;
}

function getCellY(c) {
    var cell = Math.floor(c / glbl.cellSize);
    return (cell >= glbl.yCellCount) ? cell - 1 : cell;
}

function getMouseX(x) {
    return (x - glbl.xOffset);
}

function getMouseY(y) {
    return (y - glbl.yOffset);
}

function getYOffset() {
    var viewportOffset = glbl.canvas.getBoundingClientRect();
    return viewportOffset.top;
}

function getXOffset() {
    var viewportOffset = glbl.canvas.getBoundingClientRect();
    return viewportOffset.left;
}

function getCellSize() {
    return Math.floor($('.container').width() / getXCellCount());
}

function getXCellCount() {
    return glbl.n;
}

function getYCellCount() {
    return Math.floor($(window).height() / glbl.cellSize);
}

function getData() {
    var json = '{"mgm": {"0": {"0": [], "1": [], "2": [], "3": [], "4": [5], "5": [5], "6": [5], "7": [5], "8": [], "9": [], "10": [], "11": [], "12": [], "13": [], "14": []}, "1": {"0": [], "1": [], "2": [], "3": [], "4": [5], "5": [5], "6": [5], "7": [5], "8": [], "9": [], "10": [], "11": [], "12": [], "13": [], "14": []}, "2": {"0": [], "1": [], "2": [], "3": [], "4": [5], "5": [5], "6": [5], "7": [5], "8": [], "9": [], "10": [], "11": [], "12": [], "13": [], "14": []}, "3": {"0": [], "1": [0], "2": [0], "3": [0], "4": [0, 5], "5": [0, 5], "6": [0, 5], "7": [5], "8": [], "9": [], "10": [], "11": [], "12": [], "13": [], "14": []}, "4": {"0": [], "1": [0], "2": [0], "3": [0], "4": [0], "5": [0], "6": [0], "7": [], "8": [], "9": [], "10": [], "11": [], "12": [], "13": [], "14": []}, "5": {"0": [], "1": [0], "2": [0], "3": [0], "4": [0], "5": [0], "6": [0], "7": [], "8": [], "9": [], "10": [], "11": [], "12": [], "13": [], "14": []}, "6": {"0": [3, 4], "1": [0, 3, 4], "2": [0, 3, 4], "3": [0, 3, 4], "4": [0, 3, 4], "5": [0, 3, 4], "6": [0, 3, 4], "7": [3, 4], "8": [3, 4], "9": [3, 4], "10": [4], "11": [], "12": [], "13": [], "14": []}, "7": {"0": [3, 4], "1": [0, 3, 4], "2": [0, 3, 4], "3": [0, 3, 4], "4": [0, 3, 4], "5": [0, 3, 4], "6": [0, 3, 4], "7": [3, 4], "8": [3, 4], "9": [3, 4], "10": [4], "11": [], "12": [], "13": [], "14": []}, "8": {"0": [3, 4], "1": [3, 4], "2": [3, 4], "3": [3, 4], "4": [3, 4], "5": [3, 4], "6": [3, 4], "7": [3, 4], "8": [3, 4], "9": [3, 4], "10": [4], "11": [], "12": [], "13": [], "14": []}, "9": {"0": [3, 4], "1": [9, 3, 4], "2": [9, 3, 4], "3": [9, 3, 4], "4": [9, 3, 4], "5": [9, 3, 4], "6": [9, 3, 4], "7": [9, 3, 4], "8": [3, 4], "9": [1, 3, 4], "10": [1, 4], "11": [1], "12": [1], "13": [1], "14": []}, "10": {"0": [3, 4], "1": [9, 3, 4], "2": [9, 3, 4], "3": [9, 3, 4], "4": [9, 3, 4], "5": [9, 3, 4], "6": [9, 3, 4], "7": [9, 3, 4], "8": [3, 4], "9": [1, 3, 4], "10": [1, 4], "11": [1], "12": [1], "13": [1], "14": []}, "11": {"0": [3], "1": [9, 3], "2": [9, 3], "3": [9, 3], "4": [9, 3], "5": [9, 3], "6": [9, 3], "7": [9, 3], "8": [3], "9": [1, 3], "10": [1], "11": [1], "12": [1], "13": [1], "14": []}, "12": {"0": [3], "1": [9, 3], "2": [9, 3], "3": [9, 3], "4": [9, 3], "5": [9, 3], "6": [9, 3], "7": [9, 3], "8": [3], "9": [1, 3], "10": [1], "11": [1], "12": [1], "13": [1], "14": []}, "13": {"0": [3], "1": [9, 3], "2": [9, 3], "3": [9, 3], "4": [9, 3], "5": [9, 3], "6": [9, 3], "7": [9, 3], "8": [3], "9": [1, 3], "10": [1], "11": [1], "12": [1], "13": [1], "14": []}, "14": {"0": [3], "1": [9, 3], "2": [9, 3], "3": [9, 2, 3], "4": [9, 2, 3], "5": [9, 2, 3], "6": [9, 2, 3], "7": [9, 2, 3], "8": [2, 3], "9": [1, 3], "10": [1], "11": [1], "12": [1], "13": [1], "14": []}, "15": {"0": [3], "1": [9, 3], "2": [9, 3], "3": [9, 2, 3], "4": [9, 2, 3], "5": [9, 2, 3], "6": [9, 2, 3], "7": [9, 2, 3], "8": [2, 3], "9": [1, 3], "10": [1], "11": [1], "12": [1], "13": [1], "14": []}, "16": {"0": [3, 7], "1": [9, 3, 7], "2": [9, 3, 7], "3": [9, 2, 3, 7], "4": [9, 2, 3, 7], "5": [9, 2, 3, 7], "6": [9, 2, 3, 7], "7": [9, 2, 3, 7], "8": [2, 3, 7], "9": [1, 3, 7], "10": [1, 7], "11": [1, 7], "12": [1], "13": [1], "14": []}, "17": {"0": [7], "1": [9, 7], "2": [9, 7], "3": [9, 2, 7], "4": [9, 2, 7], "5": [9, 2, 7], "6": [9, 2, 7], "7": [9, 2, 7], "8": [2, 7], "9": [1, 7], "10": [1, 6, 7], "11": [1, 6, 7], "12": [1], "13": [1], "14": []}, "18": {"0": [7], "1": [9, 7], "2": [9, 7], "3": [9, 7], "4": [9, 7], "5": [9, 7], "6": [9, 7], "7": [9, 7], "8": [7], "9": [7], "10": [6, 7], "11": [6, 7], "12": [], "13": [], "14": []}, "19": {"0": [7], "1": [7], "2": [7], "3": [7], "4": [8, 7], "5": [8, 7], "6": [8, 7], "7": [8, 7], "8": [8, 7], "9": [8, 7], "10": [8, 6, 7], "11": [8, 6, 7], "12": [8], "13": [8], "14": [8]}, "20": {"0": [7], "1": [7], "2": [7], "3": [7], "4": [8, 7], "5": [8, 7], "6": [8, 7], "7": [8, 7], "8": [8, 7], "9": [8, 7], "10": [8, 6, 7], "11": [8, 6, 7], "12": [8], "13": [8], "14": [8]}, "21": {"0": [7], "1": [7], "2": [7], "3": [7], "4": [8, 7], "5": [8, 7], "6": [8, 7], "7": [8, 7], "8": [8, 7], "9": [8, 7], "10": [8, 6, 7], "11": [8, 6, 7], "12": [8], "13": [8], "14": [8]}, "22": {"0": [7], "1": [7], "2": [7], "3": [7], "4": [8, 7], "5": [8, 7], "6": [8, 7], "7": [8, 7], "8": [8, 7], "9": [8, 7], "10": [8, 6, 7], "11": [8, 6, 7], "12": [8], "13": [8], "14": [8]}, "23": {"0": [7], "1": [7], "2": [7], "3": [7], "4": [8, 7], "5": [8, 7], "6": [8, 7], "7": [8, 7], "8": [8, 7], "9": [8, 7], "10": [8, 7], "11": [8, 7], "12": [8], "13": [8], "14": [8]}, "24": {"0": [], "1": [], "2": [], "3": [], "4": [8], "5": [8], "6": [8], "7": [8], "8": [8], "9": [8], "10": [8], "11": [8], "12": [8], "13": [8], "14": [8]}, "25": {"0": [], "1": [], "2": [], "3": [], "4": [8], "5": [8], "6": [8], "7": [8], "8": [8], "9": [8], "10": [8], "11": [8], "12": [8], "13": [8], "14": [8]}, "26": {"0": [], "1": [], "2": [], "3": [], "4": [8], "5": [8], "6": [8], "7": [8], "8": [8], "9": [8], "10": [8], "11": [8], "12": [8], "13": [8], "14": [8]}, "27": {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [], "6": [], "7": [], "8": [], "9": [], "10": [], "11": [], "12": [], "13": [], "14": []}}}'
    //var json = '{"mgm": {"0": {"0": [1], "1": [1], "2": []}, "1": {"0": [1], "1": [1, 9], "2": [9]}, "2": {"0": [], "1": [9], "2": [9]}}}';
    obj = JSON.parse(json);
    return obj.mgm;
}
