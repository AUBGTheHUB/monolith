import { Fragment } from 'react/jsx-runtime';
import { Link } from 'react-router';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Helmet } from 'react-helmet';
import { toast } from 'react-toastify';
import teamMembers from './resources/teamMembers.json';

export function MeetTheTeamPage() {
    const handleDelete = (id: string, name: string) => {
        if (window.confirm(`Are you sure you want to delete ${name}?`)) {
            console.log('Deleting team member:', id);
            toast.success(`${name} has been deleted successfully!`);
        }
    };

    return (
        <Fragment>
            <Helmet>
                <title>Meet the Team - Admin Panel</title>
                <link rel="icon" href="/faviconHack.ico" />
            </Helmet>
            <div className="min-h-screen bg-gray-50 p-8">
                <div className="max-w-7xl mx-auto">
                    <div className="flex justify-between items-center mb-8">
                        <div>
                            <h1 className="text-4xl font-bold">Meet the Team</h1>
                            <p className="text-gray-600 mt-2">Manage team members</p>
                        </div>
                        <Link to="/dashboard/meet-the-team/add">
                            <Button className="bg-blue-600 hover:bg-blue-700 text-lg px-6 py-6">+ Add Member</Button>
                        </Link>
                    </div>

                    {teamMembers.length === 0 ? (
                        <div className="text-center py-12 bg-white rounded-lg shadow">
                            <p className="text-gray-500 mb-4 text-lg">No team members yet</p>
                            <Link to="/dashboard/meet-the-team/add">
                                <Button className="bg-blue-600 hover:bg-blue-700">Add Your First Member</Button>
                            </Link>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {teamMembers.map((member) => (
                                <Card key={member.id} className="overflow-hidden hover:shadow-lg transition-shadow">
                                    <CardHeader className="p-0">
                                        <img
                                            src={member.image}
                                            alt={member.name}
                                            className="w-full h-64 object-cover"
                                        />
                                    </CardHeader>
                                    <CardContent className="pt-4 pb-3">
                                        <CardTitle className="mb-2">{member.name}</CardTitle>
                                        <div className="flex flex-wrap gap-2">
                                            {member.departments.map((dept) => (
                                                <span
                                                    key={dept}
                                                    className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                                                >
                                                    {dept}
                                                </span>
                                            ))}
                                        </div>
                                    </CardContent>
                                    <CardFooter className="flex gap-2">
                                        <Button
                                            variant="destructive"
                                            className="flex-1 bg-red-600 hover:bg-red-700"
                                            onClick={() => handleDelete(member.id, member.name)}
                                        >
                                            Delete
                                        </Button>
                                        <Link to={`/dashboard/meet-the-team/${member.id}`} className="flex-1">
                                            <Button variant="outline" className="w-full">
                                                Edit
                                            </Button>
                                        </Link>
                                    </CardFooter>
                                </Card>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </Fragment>
    );
}
