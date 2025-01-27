let $ = document ;
let submitBtn = $.getElementById('submit-btn')
let name = $.getElementById('name-input')
let popUp = $.getElementsByClassName('modal')[0]
let form = $.getElementsByTagName('form') ;
submitBtn.addEventListener('click' , async (e) => {
    e.preventDefault()
    let result = await fetch(`/blog/getUser/${name.value}/` , {
        method : "GET" ,
    })
    console.log(result)
    let data = await result.json()
    console.log(data)
    if (data['message'] == 'this username already taken'){
         popUp.classList.add('active-modal')
         popUp.innerText = data['message']
         setTimeout(()=>{
              popUp.classList.remove('active-modal')
         },2000)
    }
    else {
         console.log(form)
         form.submit()
    }
})