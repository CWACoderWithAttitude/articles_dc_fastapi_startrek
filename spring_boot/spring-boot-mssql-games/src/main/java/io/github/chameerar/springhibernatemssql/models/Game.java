package io.github.chameerar.springhibernatemssql.models;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Entity
@Getter
@Setter
@ToString
public class Game {

    @Id
    @GeneratedValue
    private Long id;
    private String title;
    private String ean13;
    private String publisher;
    private String genre;
    private Integer minNumberofPlayers;
    private Integer maxNumberofPlayers;
    private Integer minAge;
    private String typical_duration;

    public Game() {
    }

    public Game(String title) {
        this.title = title;
    }
}
