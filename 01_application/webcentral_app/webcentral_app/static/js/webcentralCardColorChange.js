function cardColorChange(perspective){
  if (perspective != "technisch"){ 
    const result = document.querySelectorAll('div.border-technical');
    for (let i = 0; i < result.length; i++) {
      const element =result[i];
      let className=element.className;
      let classNameArray = className.split(' ');
      classNameArray.splice(classNameArray.indexOf('border-technical'),1);
      if (perspective == "ökologisch"){
        element.className = classNameArray.join(' ') + ' border-ecological';
      }   
      if (perspective == "rechtlich"){
        element.className = classNameArray.join(' ') + ' border-legal';   
      } 
      if (perspective == "betrieblich"){
        element.className = classNameArray.join(' ') + ' border-operational';   
      } 
    } 
  }
} 