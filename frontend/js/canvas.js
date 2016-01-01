var glbl = (function() {
    var canvas;
    var padding;
    var width, height;
    var xOffset, yOffset;
    var xCellCount, yCellCount;
    var gridCount;
    var url = 'http://localhost:5000';
    var data;
    var context;
    var cellSize = 40;
    var values = [];
    var colors = [[0, 51, 153], [0, 102, 0], [153, 0, 0], [153, 102, 0], [0, 153, 255], [102, 204, 51], [255, 153, 51], [102, 102, 204], [255, 51, 0], [255, 255, 0]];
    return {
        canvas: canvas,
        padding: padding,
        width: width,
        height: height,
        xOffset: xOffset,
        yOffset: yOffset,
        xCellCount: xCellCount,
        yCellCount: yCellCount,
        gridCount: gridCount,
        url: url,
        context: context,
        cellSize: cellSize,
        values: values,
        colors: colors,
        data: data,
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

(function(window) {
    $(document).ready(function($) {
        var timer = null;    
        initGrid();

        /*$('canvas').get(0).addEventListener('mousedown', function(e) {
            var cx = getCellX(getMouseX(e.pageX));
            var cy = getCellY(getMouseY(e.pageY));
            showPairsAtTile(cx, cy);
        }); */      

        $('#next-button').get(0).addEventListener('click', function(e) {
            getUpdatedData();
        });

        $('#start-button').get(0).addEventListener('click', function(e) {
            if (!timer) {
                timer = setInterval(getUpdatedData, 1000);
            }
        });

        $('#pause-button').get(0).addEventListener('click', function(e) {
            if (timer) {
                clearInterval(timer);
                timer = null;
            }
        });

        $('#reset-button').get(0).addEventListener('click', function(e) {
            getData();
        });
    });
}(window));

/*function showPairsAtTile(cx, cy) {
    if (cx != null && cy != null) {
        $('#tile-id').text(glbl.data.mgm[cx][cy]);
    }
}*/

function initGrid() {
    setPrivateProperties();
    getData();
}

function setPrivateProperties() {
    glbl.xCellCount = getXCellCount();
    glbl.yCellCount = getYCellCount();
    glbl.width = glbl.xCellCount * glbl.cellSize;
    glbl.height = glbl.yCellCount * glbl.cellSize;
    glbl.padding = 0;
    var cw = glbl.width + (glbl.padding*2) + 1;
    var ch = glbl.height + (glbl.padding*2) + 1;

    glbl.canvas = $('<canvas/>').attr({width: cw, height: ch}).appendTo('#canvas-container').get(0);
    glbl.context = glbl.canvas.getContext("2d");
    glbl.xOffset = getXOffset();
    glbl.yOffset = getYOffset();
}

function drawGrid() {
    glbl.context.clearRect(0, 0, glbl.width, glbl.height);
    glbl.context.beginPath();
    glbl.context.lineWidth = 1;
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
    drawGrid();
    for (var i = 0; i < data.length; i += 1) {
        min_x = getAbsPosX(getCellX(data[i][0]));
        min_y = getAbsPosY(getCellY(data[i][1]));
        max_x = getAbsPosX(getCellX(data[i][2])) + glbl.cellSize;
        max_y = getAbsPosY(getCellY(data[i][3])) + glbl.cellSize;
        drawRect(min_x, min_y, max_x - min_x, max_y - min_y, i);
    }
}

function drawObjects(data) {
    glbl.context.lineWidth = 1;
    for (var i = 0; i < data.length; i += 1) {
        for (var j = 0; j < data[i].length; j += 1) {
            glbl.context.beginPath();
            glbl.context.arc(data[i][j][0], data[i][j][1], glbl.cellSize/20, 0, 2*Math.PI);
            glbl.context.closePath();
            glbl.context.fillStyle = 'rgb(' + [glbl.colors[i][0], glbl.colors[i][1], glbl.colors[i][2]].join(',') + ')';
            glbl.context.strokeStyle = 'rgb(' + [glbl.colors[i][0], glbl.colors[i][1], glbl.colors[i][2]].join(',') + ')';
            glbl.context.stroke();
            glbl.context.fill();
        }
    }
}

function drawRect(min_x, min_y, max_x, max_y, color) {
    glbl.context.lineWidth = 3;
    glbl.context.strokeStyle = 'rgb(' + [glbl.colors[color][0], glbl.colors[color][1], glbl.colors[color][2]].join(',') + ')';
    glbl.context.strokeRect(min_x - 1, min_y - 1, max_x, max_y);
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

function getXCellCount() {
    return Math.floor(($(window).width() - 180) / glbl.cellSize);
}

function getYCellCount() {
    return Math.floor(($(window).height() - 40)/ glbl.cellSize);
}

function getData() {
    $.getJSON([glbl.url, "init-grid", 2, glbl.width, glbl.height, "abc"].join('/'), function(data) {
        preserveData(data);
        fillGrid(data.boxes);
        drawObjects(data.objects);
    });
}

function getUpdatedData() {
    var token = "abc";
    $.getJSON([glbl.url, "move-objects", token].join('/'), function(data) {
        preserveData(data);
        fillGrid(data.boxes);
        drawObjects(data.objects);
        showTimes(data.times);
    });
}

function showTimes(data) {
    matrix = data[0];
    hashed = data[1];
    $('#matrix-time').text(matrix);
    $('#hashed-time').text(hashed);
}

function preserveData(data) {
    glbl.data = null;
    glbl.data = data;
}
