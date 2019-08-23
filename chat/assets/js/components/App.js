import React, { Component} from "react"

class App extends Component {

  constructor (props) {
    super(props)
    this.state = {
      text: '',
      conversation: []
    }
  }

  handleTextChange (e) {
    this.setState({text: e.target.value})
  }

  handleSubmit (e) {
    e.preventDefault()

    let text = this.state.text.trim()
    if (!text) {
      return
    }

    const apiUrl = '/api/chatbot/'

    const headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }

    const params = {
      method: 'POST',
      body: JSON.stringify({text: text}),
      headers
    }

    fetch(apiUrl, params)
      .then(response => response.json())
      .then(result => {
        let conversation = this.state.conversation
        conversation.push({
          type: 'chat__item--user',
          text: this.state.text
        })
        conversation.push({
          type: 'chat__item--chatbot',
          text: result.text
        })
        this.setState({
          conversation: conversation,
          text: ''
        })
      }, error => {
        this.setState({ error })
      }
    )
  }

  render() {
    const { conversation, text } = this.state

    return(
      <div className='row chat'>
        <div className='col-md-6 offset-md-3'>
          {
            conversation.map((item, i) => {
              return <div className={item.type} key={i}>{item.text}</div>
            })
          }
        <form className="chat__item--user" onSubmit={this.handleSubmit.bind(this)}>
          <div className="form-group">
            <textarea
              className="form-control"
              placeholder={gettext('Ask something')}
              onChange={this.handleTextChange.bind(this)} required="required" value={text}
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
