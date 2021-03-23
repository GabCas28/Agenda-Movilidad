var HelloButton = function (context) {
    var ui = $.summernote.ui;
  
    // create button
    var button = ui.button({
      contents: '<i class="fa fa-child"/> Hello',
      tooltip: 'hello',
      click: function () {
        // invoke insertText method with 'hello' on editor module.
        context.invoke('editor.insertText', 'hello');
      }
    });
  
    return button.render();   // return button as jquery object
  }
  $('#summernote').summernote({
    toolbar: [
      ['mybutton', ['hello']]
    ],
  
    buttons: {
      hello: HelloButton
    }
  });