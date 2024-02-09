import TeamIcon from "@/components/team/TeamIcon";
import { Team, TeamMember } from "@/utils/django_types";
import axios from "axios";
import { useEffect, useState } from "react";
import { BeatLoader } from "react-spinners";

const TEAM_ID = window.location.pathname.split("/").pop();

export default function TeamPage() {

  const [team,  setTeam] = useState<Team>();
  const [members, setMembers] = useState<TeamMember[]>();
  const [loadingData, setLoadingData] = useState(true);

  useEffect(() => {
    setLoadingData(true);
    console.log("team_id:",TEAM_ID);
    axios.get(`/api/teams/${TEAM_ID}`).then((response) => {
      console.log(response.data);
      setTeam(response.data as Team);
      setLoadingData(false);
    }).catch((error) => {
      alert("Could not find team.")
      window.location.assign("/");
      console.error(error);
    });
    axios.get(`/api/teams/${TEAM_ID}/members`).then((response) => {
      console.log(response.data);
      setMembers(response.data as TeamMember[]);
    }).catch((error) => {
      console.error(error);
    });
  },[])

  return (
    <div className="teampage text-center text-white pt-6 min-h-[90vh]">
      { loadingData ? <BeatLoader className="justify-center content-center pr-2" color={'#fff'} size={12} /> : 
        <div className="teampage-content">
          <TeamIcon className="w-24 h-24 mx-auto text-center" color={team?.color_choice ?? ""} emoji={team?.emoji_choice ?? ""} emoji_cn="text-6xl"/>
          <h1 className="text-4xl font-bold text-center pt-5 pb-7">{team?.team_name}</h1>
          <h1 className="text-center font-bold text-xl">{members?.length ?? 0} Member{members?.length !== 1 ? 's' : ''}</h1>
        </div>}
      
    </div>
  )
}