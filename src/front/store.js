export const initialStore=()=>{
  return{
    message: null,
    todos: [
      {
        id: 1,
        title: "Make the bed",
        background: null,
      },
      {
        id: 2,
        title: "Do my homework",
        background: null,
      }
    ]
  }
}

export default function storeReducer(store, action = {}) {
  switch(action.type){
    case 'set_hello':
      return {
        ...store,
        message: action.payload
      };
      
    case 'login':

       return {
        ...store,
        isAuth: true
      };

    case 'logout':

      return {
        ...store,
        isAuth: false
      };

    default:
      throw Error('Unknown action.');
  }    
}
