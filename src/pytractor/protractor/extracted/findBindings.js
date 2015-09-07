try { return (function (binding, exactMatch, using, rootSelector) {
  var root = document.querySelector(rootSelector || 'body');
  using = using || document;
  if (angular.getTestability) {
    return angular.getTestability(root).
        findBindings(using, binding, exactMatch);
  }
  var bindings = using.getElementsByClassName('ng-binding');
  var matches = [];
  for (var i = 0; i < bindings.length; ++i) {
    var dataBinding = angular.element(bindings[i]).data('$binding');
    if (dataBinding) {
      var bindingName = dataBinding.exp || dataBinding[0].exp || dataBinding;
      if (exactMatch) {
        var matcher = new RegExp('({|\\s|^|\\|)' +
            /* See http://stackoverflow.com/q/3561711 */
            binding.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, '\\$&') +
            '(}|\\s|$|\\|)');
        if (matcher.test(bindingName)) {
          matches.push(bindings[i]);
        }
      } else {
        if (bindingName.indexOf(binding) != -1) {
          matches.push(bindings[i]);
        }
      }

    }
  }
  return matches; /* Return the whole array for webdriver.findElements. */
}).apply(this, arguments); }
catch(e) { throw (e instanceof Error) ? e : new Error(e); }