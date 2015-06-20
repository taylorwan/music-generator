window.onload = init;
var context;
var bufferLoader;
var RhythmSample = {
};

function init() {
  // Fix up prefixing
  window.AudioContext = window.AudioContext || window.webkitAudioContext;
  context = new AudioContext();

  bufferLoader = new BufferLoader(
    context,
    [
      '../examples/7.wav',
      '../examples/5.wav',
      '../examples/2.wav',
    ],
    finishedLoading
    );
  bufferLoader.load();

}

function finishedLoading(bufferList) {
  // Create two sources and play them both together.
  var source1 = context.createBufferSource();
  var source2 = context.createBufferSource();
  source1.buffer = bufferList[0];
  source2.buffer = bufferList[1];

  source1.connect(context.destination);
  source2.connect(context.destination);
  source1.start(0);
  source2.start(0);
}

function BufferLoader(context, urlList, callback) {
  this.context = context;
  this.urlList = urlList;
  this.onload = callback;
  this.bufferList = new Array();
  this.loadCount = 0;
}

// buffer loader classes

BufferLoader.prototype.loadBuffer = function(url, index) {
  // Load buffer asynchronously
  var request = new XMLHttpRequest();
  request.open("GET", url, true);
  request.responseType = "arraybuffer";

  var loader = this;

  request.onload = function() {
    // Asynchronously decode the audio file data in request.response
    loader.context.decodeAudioData(
      request.response,
      function(buffer) {
        if (!buffer) {
          alert('error decoding file data: ' + url);
          return;
        }
        loader.bufferList[index] = buffer;
        if (++loader.loadCount == loader.urlList.length)
          loader.onload(loader.bufferList);
      },
      function(error) {
        console.error('decodeAudioData error', error);
      }
    );
  }

  request.onerror = function() {
    alert('BufferLoader: XHR error');
  }

  request.send();
}

BufferLoader.prototype.load = function() {
  for (var i = 0; i < this.urlList.length; ++i)
  this.loadBuffer(this.urlList[i], i);
}

// player code

RhythmSample.play = function() {
  function playSound(buffer, time) {
    var source = context.createBufferSource();
    source.buffer = buffer;
    source.connect(context.destination);
    if (!source.start)
      source.start = source.noteOn;
    source.start(time);
  }

  var kick = bufferLoader.bufferList[0];
  var snare = bufferLoader.bufferList[1];
  var hihat = bufferLoader.bufferList[2];

  // We'll start playing the rhythm 100 milliseconds from "now"
  var startTime = context.currentTime + 0.100;
  var kicks = [1.0, 2.0, 3.0, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5];
  var snares = [0.5, 1.5, 2.5, 3.5, 4.5, 5.0, 5.5, 6.0, 6.5];
  for (var hit = 0; hit < kicks.length; hit++){
    playSound(kick, kicks[hit]);
  }
  for (var hit = 0; hit < snares.length; hit++){
    playSound(snare, snares[hit]);
  }

};
