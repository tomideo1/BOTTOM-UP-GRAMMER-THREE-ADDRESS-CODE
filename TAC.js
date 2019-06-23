
var numbers = /^\d+$/;
var symbols = /^(\+|-|\*|\/|=|>|<|>=|<=|&|\||%|!|\^|\(|\))$/;
var identifier = /^[a-zA-Z]+$/;

var symbol_table = {
    ")": {
        "level": -2, "association": "left", "unary": false},
    "=": {
        "level": -1, "association": "right", "unary": false},
    "^": {
        "level": 6, "association": "right", "unary": false},
    "~": {
        "level": 5, "association": "right", "unary": true},
    "/": {
        "level": 3, "association": "left", "unary": false},
    "*": {
        "level": 3, "association": "left", "unary": false},
    "-": {
        "level": 2, "association": "left", "unary": false},
    "+": {
        "level": 2, "association": "left", "unary": false},
    "(": {
        "level": 0, "association": "left", "unary": false},

};


class Address{
    constructor (identifier, operator, arg1, arg2="", unary=false){
        this.identifier = identifier;
        this.operator = operator;
        this.arg1 = arg1;
        this.arg2 = arg2;
        this.unary = unary;
    }

}

function verifyNum(string){
    if(isNaN(string) == false){
        return true
    }
    return false

}
function veryfyOp(string){
    if(symbols.test(string)){
        return true
    }
    return false
}

function isidentifier(string){
    if(identifier.test(string)){
        return true
    }
    return false
}

function dev_token(string){
    var token_arr = []
    var last_element = string.length + 1
    var i =0, j = 1;
    while(j != last_element){
        var sub_element = string.slice(i,j)
        if(sub_element ==" "){
            i++
            j++
            continue;
        }
           if(isidentifier(sub_element)){
               while(isidentifier(sub_element)){
                   j++
                   sub_element = string.slice(i,j)
                   if(j == last_element){
                       break;
                   }
               }
               j--
               sub_element = string.slice(i,j)
               token_arr.push(sub_element)
               i = j
               j++
               continue;
        }
        if(verifyNum(sub_element)){
            while(verifyNum(sub_element)){
                j++
                sub_element = string.slice(i,j)
                if(j == last_element){
                    break;
                }

            }
            j--
            sub_element = string.slice(i,j)
            token_arr.push(sub_element)
            i = j
            j++
            continue;
        }

        if(veryfyOp(sub_element)){
            token_arr.push(sub_element)
            i++
            j++
            continue;
        }
    }

    for(var k = 0; k< token_arr.length; k++){
        if(token_arr[k] == "-"){
            if(k == 0){
                token_arr[k] = '~'
            }
            else{
                var prev = token_arr[k-1]
                if( (prev != ')') && !(isidentifier(prev)) && !(verifyNum(prev))){
                    token_arr[k] = '~'
                }
            }
        }
    }

    return token_arr
}


function con_inf_post(tokens){
    var output_stack = []
    var operator_stack = []
    tokens.forEach(token =>{
        if(isidentifier(token) || verifyNum(token)){
            output_stack.push(token)
        }
        else if(token == "(" ){
            operator_stack.push(token)
        }
        else if(token == ")" ){
            while(operator_stack[operator_stack.length-1] != "("){
                if(operator_stack.length != 0 ){
                    var temp = operator_stack.pop()
                    output_stack.push(temp)
                }
                else{
                    document.getElementById('errors').innerHTML = "Exception"
                }
            }
            operator_stack.pop()
        }
        else{
            while(true){
                var j = (operator_stack.length) - 1
                if(j != -1){
                    var token_precedence = symbol_table[token]['level']
                    var top_precedence = symbol_table[operator_stack[j]]['level']
                    var token_assoc = symbol_table[token]['assocoation']
                    if (((top_precedence > token_precedence)
                         || ((top_precedence == token_precedence) && token_assoc == "left"))
                            &&
                            (operator_stack[j] != "(")
                    )
                    {
                        temp2 = operator_stack.pop()
                      output_stack.push(temp2)
                    }
                    else{
                      break;
                    }

                }
                else{
                  break;
                }
            }
            operator_stack.push(token)
        }
    })
    while (operator_stack.length > 0 ) {
        if(operator_stack[operator_stack.length-1] == "("){
            document.getElementById('errors').innerHTML = "this can't be done"
        }
        temp3 = operator_stack.pop()
        output_stack.push(temp3)
    }
return output_stack
}


function evauluate_string(tokens){
    var final_output = []
    var index = 0 
    var address_field = []
    tokens.forEach(token => {
        if(isidentifier(token) || verifyNum(token)){
            final_output.push(token)
        }
        else{
            if(symbol_table[token]['unary']){
                id = "T"+index
                end = final_output.pop()
                line = new Address(id,token,end,'',unary=true)
                address_field.push(line)
                final_output.push(id)
                index++
            }
            else{
                id = "T"+index
                b= final_output.pop()
                a= final_output.pop()
                line = null
                if(token == "="){
                    id = a
                    line = new Address(id,token,b,'')

                }
                else{
                    line = new Address(id,token,a,b)
                }
                address_field.push(line)
                final_output.push(id)
                index++
            }
        }
    });
    return address_field    
}

function print_TAC(address_field){
    console.log('3 Address Code' + '\n')
    var output_stack = []
    address_field.forEach(address=> {
        // console.log(address)
        if(symbol_table[address['operator']]['unary'] == true){
            console.log(
                 address['identifier'] + ':='
                 +address['operator']
                 + address['arg1']
                 + address['arg2']

            )
           
        }
        else if(address['operator'] == '='){
            console.log(
                address['identifier'] + ':='
                + address['arg1']

           )
        }
        else{
            console.log(
                address['identifier'] + ':='
                + address['arg1']
                +address['operator']
                + address['arg2']

           )
            }
    });
}

function  print_QUAD(address_field){
    console.log('\n' + 'Quadruple')
    index = 0 
    var output_stack = []
    console.log('\t' + 'OP'+ '\t' + 'ARG1' + '\t' + 'ARG2' + '\t' + 'RESULT')
    for(var i = 0; i<address_field.length; i++){
        console.log('('+index +')'
        + '\t'+ address_field[i]['operator'] 
        + '\t' + address_field[i]['arg1']
        +'\t'  + address_field[i]['arg2']
        + '\t' +  address_field[i]['identifier']
        )
            index++
    }
    return output_stack
}

function print_TRIPLE(address_field){
    console.log('\n' + 'TRIPLE')
    var index = 0 
    var id
    var output_stack = []
    console.log('\t' + 'OP'+ '\t' + 'ARG1' + '\t' + 'ARG2')
    for(var i = 0; i<address_field.length; i++){
        var arg1 = address_field[i]['arg1']
        var arg2 = address_field[i]['arg2']
        console.log('('+index +')' + '\t' + address_field[i]['operator'] + '\t' + 
        (arg1.includes('T')? '(' +arg1.slice(1) + ')':arg1) + '\t'
        + (arg2.includes('T')? '('+ arg2.slice(1) +')':arg2 )
        )
       
            index++
    }
    return output_stack
}
// st = "e ^ x = 1 + x / 1 + x ^ 2 / 2 "
st= "-b + -( b ^2 - 4 *a*c)^ 0.5 /2*a "
tok = dev_token(st)
console.log(''+tok + '\n')
pos = con_inf_post(tok)
console.log(''+pos + '\n')
tac = evauluate_string(pos)
print_TAC(tac)
print_QUAD(tac)
print_TRIPLE(tac)

