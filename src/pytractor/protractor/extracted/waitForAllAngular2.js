try { return (function (callback) {
  try {
    var testabilities = window.getAllAngularTestabilities();
    var count = testabilities.length;
    var decrement = function() {
      count--;
      if (count === 0) {
        callback();
      }
    };
    testabilities.forEach(function(testability) {
      testability.whenStable(decrement);
    });
  } catch (err) {
    callback(err.message);
  }
}).apply(this, arguments); }
catch(e) { throw (e instanceof Error) ? e : new Error(e); }