try { return (function (searchText, using) {
  using = using || document;
  var elements = using.querySelectorAll('button, input[type="button"], input[type="submit"]');
  var matches = [];
  for (var i = 0; i < elements.length; ++i) {
    var element = elements[i];
    var elementText;
    if (element.tagName.toLowerCase() == 'button') {
      elementText = element.innerText || element.textContent;
    } else {
      elementText = element.value;
    }
    if (elementText === searchText) {
      matches.push(element);
    }
  }

  return matches;
}).apply(this, arguments); }
catch(e) { throw (e instanceof Error) ? e : new Error(e); }