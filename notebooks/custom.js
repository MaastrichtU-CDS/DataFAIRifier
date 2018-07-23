require(['notebook/js/codecell'], function(codecell) {
  codecell.CodeCell.options_default.highlight_modes['magic_text/x-mssql'] = {'reg':[/^%%sql/]} ;
  console.log('AAAAA');
  Jupyter.notebook.events.one('kernel_ready.Kernel', function(){
      console.log('BBBBB');
      Jupyter.notebook.get_cells().map(function(cell){
          if (cell.cell_type == 'code'){ cell.auto_highlight(); } }) ;
  });
});
