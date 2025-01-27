let template = document.createElement('template') ;
template.innerHTML = `
    <link rel="stylesheet" href="/static/components/new/new-component-style.css">
    <div id="new">
          <div id="image-section">
                <slot name="new-image" id="new-image"></slot>
           </div>
           <slot id="new-title" name="new-title"></slot>
           <a id="new-body">
                 <slot name="new-body"></slot>
           </a>
           <div id="stats">
                 <div id="creator">
                        <img id="pencil" src="/static/media/logo's/pencil-crayon.png">
                        <slot name="writer-name" id="creator-name"></slot>
                  </div>
                  <div id="date">
                       <img src="/static/media/logo's/calendar.png" id="calendar">
                       <slot id="date-text" name="date"></slot>
                  </div>
           </div>
    </div>
`


export class New extends HTMLElement {
    constructor(){
        super()
        this.attachShadow({mode : 'open'})
        this.shadowRoot.appendChild(template.content.cloneNode(true))
    }
}


