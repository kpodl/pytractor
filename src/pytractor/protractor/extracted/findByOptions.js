try { return (function (optionsDescriptor, using) {
  using = using || document;

  var prefixes = ['ng-', 'ng_', 'data-ng-', 'x-ng-', 'ng\\:'];
  for (var p = 0; p < prefixes.length; ++p) {
    var selector = '[' + prefixes[p] + 'options="' + optionsDescriptor + '"] option';
    var elements = using.querySelectorAll(selector);
    if (elements.length) {
      return elements;
    }
  }
}).apply(this, arguments); }
catch(e) { throw (e instanceof Error) ? e : new Error(e); }