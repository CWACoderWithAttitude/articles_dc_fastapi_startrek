package io.github.chameerar.springhibernatemssql.controllers;

import io.github.chameerar.springhibernatemssql.models.Book;
import io.github.chameerar.springhibernatemssql.models.Game;
import io.github.chameerar.springhibernatemssql.services.BookService;
import io.github.chameerar.springhibernatemssql.services.GameService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.http.ResponseEntity;
import java.util.List;

@RestController
@RequestMapping("games")
public class GameController {
    @Autowired
    GameService gameService;

    @Value("classpath:rules_of_acquisiton.json")
    // @Value("classpath:roa.json")
    Resource resource; // = new ClassPathResource("rules_of_acquisiton.json");

    @GetMapping(value = "/", produces = "application/json")
    public List<Game> getGames() {
        return gameService.list();
    }

    @PostMapping(value = "/new", consumes = "application/json", produces = "application/json")
    public Game save(@RequestBody Game game) {
        return gameService.save(game);
    }

    @GetMapping(value = "/{id}", produces = "application/json")
    public Game get(@PathVariable Long id) {
        return gameService.get(id);
    }

    @PutMapping(value = "/{id}", consumes = "application/json", produces = "application/json")
    public Game update(@PathVariable Long id, @RequestBody Game game) {
        return gameService.update(id, game);
    }

    @DeleteMapping(value = "/{id}", produces = "application/json")
    public ResponseEntity delete(@PathVariable Long id) {
        try {
            gameService.delete(id);
            return ResponseEntity.noContent().build();
        } catch (IllegalArgumentException e) {
            return ResponseEntity.notFound().build();
        }
    }
}
