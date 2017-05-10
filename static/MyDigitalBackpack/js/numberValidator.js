function verifyNumber(number){

  //make sure the number is at least 10 digits
  if (number.length < 10) {
    return false;
  }

  //check for letters
  if (number.match(/[a-z]/i)){
    return false;
  }

  //remove dashes and parentheses
  number = number.replace(/[()-\s]/g, '')

  //starts with +1 and is length 12
  if ((number.substring(0, 2) == "+1") && (number.length == 12)){
    return number
  }

  //starts with 1 and is length 11
  if ((number.substring(0, 1) == "1") && (number.length == 11)) {
    return "+" + number
  }

  //if we have processed the number and it is still greater than 10, it is not valid
  if (number.length > 10){
    return false
  }

  //valid number but doesn't start with '+1'
  return "+1" + number

}
