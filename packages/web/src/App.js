import React from 'react'
import {
  Routes,
  Route
} from 'react-router-dom'
import LandingHome from './components/spa/landing_home_page'
import LandingAdminPage from './components/admin_page/landing_admin_page'
import Dashboard from './components/admin_page/admin_dashboard'
import Members from './components/admin_page/members_page/members'
import MemberActions from './components/admin_page/members_page/single_member'
import AddMember from './components/admin_page/members_page/new_member'

function App () {
  return (
    <Routes>
    <Route path="/" element={<LandingHome/>}/>
    <Route path="/admin" element={<LandingAdminPage/>}/>
    <Route path="/admin/dashboard" element={<Dashboard/>}/>
    <Route path="/admin/dashboard/members" element={<Members/>}/>
    <Route path="/admin/dashboard/members/actions" element={<MemberActions/>}/>
    <Route path="/admin/dashboard/members/add" element={<AddMember/>}/>
    </Routes>
  )
}

export default App
