package com.example.spring_boot_postgresql_crud.controller;

import com.example.spring_boot_postgresql_crud.model.RoADTO;
import com.example.spring_boot_postgresql_crud.repository.RoARepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
class RoAControllerE2ETest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private RoARepository roaRepository;

    @Autowired
    private ObjectMapper objectMapper;

    @BeforeEach
    void setup() {
        roaRepository.deleteAll();
    }

    @Test
    void testCreateRoAAndGetAll() throws Exception {
        RoADTO dto = new RoADTO(null, "Test Rule", 123L, "Test Comment");

        // Create
        String response = mockMvc.perform(post("/api/roa")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(dto)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.rule").value("Test Rule"))
                .andExpect(jsonPath("$.ruleNumber").value(123))
                .andExpect(jsonPath("$.comment").value("Test Comment"))
                .andReturn().getResponse().getContentAsString();

        RoADTO created = objectMapper.readValue(response, RoADTO.class);

        // Get All
        mockMvc.perform(get("/api/roa"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].id").value(created.id()))
                .andExpect(jsonPath("$[0].rule").value("Test Rule"));
    }

    @Test
    void testDeleteRule() throws Exception {
        RoADTO dto = new RoADTO(null, "To Delete", 321L, "Delete Comment");
        RoADTO created = objectMapper.readValue(
                mockMvc.perform(post("/api/roa")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(dto)))
                        .andReturn().getResponse().getContentAsString(),
                RoADTO.class);

        // Delete
        mockMvc.perform(delete("/api/roa/{id}", created.id()))
                .andExpect(status().isNoContent());

        // Confirm deletion
        List<RoADTO> all = roaRepository.findAll().stream()
                .map(r -> new RoADTO(r.getId(), r.getRule(), r.getRuleNumber(), r.getComment()))
                .toList();
        assertThat(all).isEmpty();
    }

    @Test
    void testSeedEndpoint() throws Exception {
        mockMvc.perform(get("/api/roa/seed"))
                .andExpect(status().isOk())
                .andExpect(content().string("Seed data loaded successfully"));

        // After seeding, there should be rules in the repository
        assertThat(roaRepository.count()).isGreaterThan(0);
    }
}