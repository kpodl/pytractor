try { return (function (selector, url) {
  var el = document.querySelector(selector);
  if (angular.getTestability) {
    return angular.getTestability(el).
        setLocation(url);
  }
  var $injector = angular.element(el).injector();
  var $location = $injector.get('$location');
  var $rootScope = $injector.get('$rootScope');

  if (url !== $location.url()) {
    $location.url(url);
    $rootScope.$digest();
  }
}).apply(this, arguments); }
catch(e) { throw (e instanceof Error) ? e : new Error(e); }