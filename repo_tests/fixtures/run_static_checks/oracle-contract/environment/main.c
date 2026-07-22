static const char *default_config = "/app/config/sim_defaults.yaml";

int main(void) {
    return default_config[0] == '/' ? 0 : 1;
}
