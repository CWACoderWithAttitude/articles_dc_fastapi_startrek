package com.example.spring_boot_postgresql_crud.controller;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.example.spring_boot_postgresql_crud.model.RoADTO;
import com.example.spring_boot_postgresql_crud.service.RoAService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import com.fasterxml.jackson.databind.ObjectMapper;

@WebMvcTest(RoAController.class)
public class RoAControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private RoAService roaService;

    @Autowired
    private ObjectMapper objectMapper;

    private RoADTO sampleRoADTO;

    @BeforeEach
    void setUp() {
        sampleRoADTO = new RoADTO(1L, "Rule 1", 1L, "This is a test rule");
    }

    @Test
    void testCreateRoA() throws Exception {
        // Mock the service behavior
        when(roaService.saveRoA(Mockito.any(RoADTO.class))).thenReturn(sampleRoADTO);

        // Perform the POST request
        mockMvc.perform(post("/api/roa")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(sampleRoADTO)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(sampleRoADTO.id()))
                .andExpect(jsonPath("$.rule").value(sampleRoADTO.rule()))
                .andExpect(jsonPath("$.ruleNumber").value(sampleRoADTO.ruleNumber()))
                .andExpect(jsonPath("$.comment").value(sampleRoADTO.comment()));
    }
}