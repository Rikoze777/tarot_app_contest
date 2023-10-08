function getPredictionInfo(type) {
    let image, title, description
    switch (type) {
      case 'daily':
        image = "ic_daily.png"
        title = "Daily"
        description = "Get daily advice"
        break;
      case 'love':
        image = "ic_love.png"
        title = "Love"
        description = "Get relationship advice"
        break;
      case 'finance':
        image = "ic_finance.png"
        title = "Finance"
        description = "Get financial advice"
        break;
      case 'advice':
        image = "ic_advice.png"
        title = "Question"
        description = "Get advice on any issue you are interested in"
        break;
      case 'yes_or_no':
        image = "ic_yes_or_no.png"
        title = "Yes or No"
        description = "Get positive or negative advice on an issue of interest"
        break;
      default:
        break;
    }
    return {
      image: image,
      title: title,
      description: description
    }
  }

  export {
    getPredictionInfo
  }