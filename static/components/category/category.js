let template = document.createElement('template') ;
template.innerHTML = `
    <link rel="stylesheet" href="/static/components/category/category-component-style.css">
    <div id="category">
           <slot name="title"></slot>
           <slot name="newsContainer"></slot>
    </div>
`


export class category extends HTMLElement {
    constructor(){
        super()
        this.attachShadow({mode : 'open'})
        this.shadowRoot.appendChild(template.content.cloneNode(true))
    }
}


