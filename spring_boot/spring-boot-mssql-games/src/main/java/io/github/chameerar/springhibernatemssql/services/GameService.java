package io.github.chameerar.springhibernatemssql.services;

import io.github.chameerar.springhibernatemssql.models.Book;
import io.github.chameerar.springhibernatemssql.models.Game;
import io.github.chameerar.springhibernatemssql.repositories.GameRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.Optional;
import java.util.logging.Logger;

@Service
public class GameService {
    Logger logger = Logger.getLogger(GameService.class.getName());
    @Autowired
    private GameRepository gameRepository;

    public List<Game> list() {
        return gameRepository.findAll();
    }

    public Game save(Game game) {
        return gameRepository.save(game);
    }

    public Game get(Long id) {
        logger.info("Game ID: " + id);
        Optional<Game> gameptional = gameRepository.findById(id);
        logger.info("Game Optional: " + gameptional);
        if (gameptional.isEmpty()) {
            logger.info("Game not found");
            throw new ResponseStatusException(
                    org.springframework.http.HttpStatus.NOT_FOUND, "Game not found");
        }
        return gameptional.get();
    }

    public Game update(Long id, Game game) {
        Optional<Game> gameOptional = gameRepository.findById(id);
        if (gameOptional.isEmpty()) {
            throw new ResponseStatusException(
                    org.springframework.http.HttpStatus.NOT_FOUND, "Game not found");
        }
        Game existingGame = gameOptional.get();
        existingGame.setTitle(game.getTitle());
        return gameRepository.save(existingGame);
    }

    public void delete(Long id) {
        gameRepository.deleteById(id);
    }
}
