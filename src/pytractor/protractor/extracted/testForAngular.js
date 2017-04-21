try { return (function (attempts, ng12Hybrid, asyncCallback) {
  var callback = function(args) {
    setTimeout(function() {
      asyncCallback(args);
    }, 0);
  };
  var check = function(n) {
    try {
      if (!ng12Hybrid && window.getAllAngularTestabilities) {
        callback({ver: 2});
      } else if (window.angular && window.angular.resumeBootstrap) {
        callback({ver: 1});
      } else if (n < 1) {
        if (window.angular) {
          callback({message: 'angular never provided resumeBootstrap'});
        } else {
          callback({message: 'retries looking for angular exceeded'});
        }
      } else {
        window.setTimeout(function() {check(n - 1);}, 1000);
      }
    } catch (e) {
      callback({message: e});
    }
  };
  check(attempts);
}).apply(this, arguments); }
catch(e) { throw (e instanceof Error) ? e : new Error(e); }