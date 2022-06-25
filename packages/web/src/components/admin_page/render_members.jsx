import React from 'react'

const RenderMembers = (members) => {
    console.log(members.members[0]["firstname"]);
    return <h1>Hello, {members.members[0]["firstname"]}!</h1>
}

export default RenderMembers