from typing import Dict, Any
from eliminationtournaments.inner_layer.entities import TournamentEntity
from eliminationtournaments.business_rules.use_cases import ( CreateTournamentUseCase, 
    FindTournamentUseCase, ListTournamentsUseCase, DeleteTournamentUseCase, UpdateTournamentUseCase )
from eliminationtournaments.outer_layer.repositories import TournamentRepository


class TournamentView:
    def __init__(self) -> None:
       self.repository = TournamentRepository()

    def list(self):
        all_tournaments_use_case = ListTournamentsUseCase(self.repository)
        tournaments = all_tournaments_use_case.execute()
        return {'message': 'Ok.', 'body': tournaments }

    def create(self, request: Dict[str, Any]):

        create_tournament_use_case = CreateTournamentUseCase()
        name = request.get('name')
        size = request.get('size')
        tournament_type = request.get('tournament_type')

        tournament_params = TournamentEntity(
          name, 
          size, 
          tournament_type, 
          status=request.get('status'),
          match_time=request.get('match_time')
        )
        tournament = create_tournament_use_case.execute(tournament_params, self.repository)
        if tournament.id:
            return { 'message': 'Created.', 'body': tournament } # body: serialize(tournament)
        return {'status': 400, 'message': 'Bad request.'}
  
    def retrieve(self, id = None):
        find_tournament_use_case = FindTournamentUseCase(self.repository)
        tournament = find_tournament_use_case.execute(id)
        return {'message': 'Ok.', 'body': tournament } # body: serialize(tournament)

    def delete(self, id = None):
      if id:
        find_tournament_use_case = DeleteTournamentUseCase(self.repository)
        tournament = find_tournament_use_case.execute(id)
        return {'status': 200, 'message': 'Ok.', 'body': tournament } 
      else:
        return {'message': 'Bad request'} 
    
    def update(self,request: Dict[str, Any], id = None):
      if id:
        find_tournament_use_case = FindTournamentUseCase(self.repository)
        tournament = find_tournament_use_case.execute(id)
        name = request.get('name')
        size = request.get('size')
        tournament_type = request.get('tournament_type')
        tournament_params = TournamentEntity(
          name, 
          size, 
          tournament_type, 
          status=request.get('status'),
          match_time=request.get('match_time')
        )

        update_tournament_use_case = UpdateTournamentUseCase(tournament, tournament_params)
        tournament = update_tournament_use_case.execute(id)

        return {'status': 200, 'message': 'Ok.', 'body': tournament } 
      else:
        return {'status': 400, 'message': 'Bad request.', 'body': tournament } 
