$(document).ready(function () {
    $(document.body).on("click","tr[data-href]", function() {
      if (this.dataset.href.includes("http")){
        window.open( this.dataset.href, '_blank');
      }
      else{
        window.location.href=this.dataset.href;
      }
    }); 
  }); 
