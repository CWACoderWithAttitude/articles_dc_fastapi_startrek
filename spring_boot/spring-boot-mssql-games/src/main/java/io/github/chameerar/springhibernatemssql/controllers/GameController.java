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

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMethod;
import jakarta.annotation.PostConstruct;
import org.apache.tomcat.util.json.JSONParser;
import org.apache.tomcat.util.json.ParseException;

@RestController
@RequestMapping("games")
public class GameController {
    @Autowired
    GameService gameService;
    java.util.logging.Logger logger = java.util.logging.Logger.getLogger(GameController.class.getName());
    @Value("classpath:board_games.json")
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

    @PostConstruct
    private void init() {
        try {
            readSeedData();
        } catch (IOException | ParseException e) {
            logger.info("Error reading seed data: " + e);
        }
    }

    /**
     * Read rule seed data from Resource and sava each rule to DB
     */
    private void readSeedData() throws IOException, ParseException {
        logger.info("seed data file: " + resource.getFilename());
        InputStream in = resource.getInputStream();
        String jsonString = new String(in.readAllBytes());
        // logger.info("seed data jsonString: " + jsonString);
        Object json = new JSONParser(jsonString).parse();
        ArrayList<Object> array = new JSONParser(jsonString).parseArray();
        // logger.info("seed data contents: " + array);
        array.forEach(item -> {
            Game g = mapToGame(item);

            logger.info("Game: {}" + g);
            gameService.save(g);
        });
    }

    private Game mapToGame(Object item) {
        Map<String, Object> map = (Map) item;
        Game g = new Game(map.get("title").toString());
        g.setEan13(map.get("ean13").toString());
        g.setPublisher(map.get("publisher").toString());
        String minPlayers = map.get("max_number_of_players").toString();
        String maxPlayers = map.get("max_number_of_players").toString();
        String minAge = map.get("min_age").toString();
        g.setMaxNumberofPlayers(Integer.parseInt(maxPlayers));
        g.setMinNumberofPlayers(Integer.parseInt(minPlayers));
        g.setMinAge(Integer.parseInt(minAge));
        // g.setGenre(map.get("genre").toString());
        // sg.setTypical_duration(map.get("typical_duration").toString());
        return g;
    }

}
