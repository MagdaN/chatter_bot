import React, { Component} from "react"
import Cookies from 'js-cookie';


const apiUrl = '/api/v1/chatbot/'

class App extends Component {

  constructor (props) {
    super(props)
    this.state = {
      conversation: [],
      text: '',
      inResponseTo: ''
    }
    this.textarea = React.createRef();
    this.handleTextChange = this.handleTextChange.bind(this)
    this.handleKeyDown = this.handleKeyDown.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  componentDidMount() {
    this.fetchResponse()
  }

  componentDidUpdate(){
     this.textarea.current.focus()
  }

  fetchResponse() {
    const { conversation, text, inResponseTo } = this.state

    const headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': Cookies.get('csrftoken')
    }

    let params = {
      method: 'GET',
      headers
    }
    if (text) {
      params = {
        method: 'POST',
        body: JSON.stringify(
          {
            text: text,
            in_response_to: inResponseTo
          }
        ),
        headers
      }
    }

    fetch(apiUrl, params)
      .then(response => response.json())
      .then(result => {
        const { conversation, text } = this.state

        if (text) {
          conversation.push({
            persona: 'client',
            text: text
          })
        }
        conversation.push({
          persona: result.persona,
          text: result.text
        })

        this.setState({
          conversation: conversation,
          text: '',
          inResponseTo: result.text
        })
      }, error => {
        this.setState({ error })
      }
    )
  }

  handleTextChange(e) {
    this.setState({ text: e.target.value })
  }

  handleKeyDown(e) {
    if(e.keyCode == 13 && e.shiftKey == false) {
      this.handleSubmit(e)
    }
  }

  handleSubmit (e) {
    e.preventDefault()

    if (!this.state.text) {
      return
    }

    this.fetchResponse()
  }

  render() {
    const { conversation, text } = this.state

    return(
      <div className='row chat'>
        <div className='col-md-6 offset-md-3'>
          {
            conversation.map((item, i) => {
              const className = item.persona == 'bot:ChatBot' ? 'chat__item--chatbot' : 'chat__item--user'
              return (
                <div key={i} className={className}>{item.text}</div>
              )
            })
          }
        <form className="chat__item--user" onSubmit={this.handleSubmit}>
          <div className="form-group">
            <textarea
              className="form-control"
              value={text}
              required="required"
              onChange={this.handleTextChange}
              onKeyDown={this.handleKeyDown}
              ref={this.textarea}
            />
          </div>
          <input type="submit" className="btn btn-primary" value={gettext('Submit')}/>
        </form>
        </div>
      </div>
    )
  }
}

export default App
