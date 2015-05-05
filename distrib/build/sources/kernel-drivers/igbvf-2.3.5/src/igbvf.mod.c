#include <linux/module.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

MODULE_INFO(vermagic, VERMAGIC_STRING);

struct module __this_module
__attribute__((section(".gnu.linkonce.this_module"))) = {
 .name = KBUILD_MODNAME,
 .init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
 .exit = cleanup_module,
#endif
 .arch = MODULE_ARCH_INIT,
};

static const struct modversion_info ____versions[]
__used
__attribute__((section("__versions"))) = {
	{ 0x7571f08, "module_layout" },
	{ 0x3ce4ca6f, "disable_irq" },
	{ 0xeaca354f, "kmalloc_caches" },
	{ 0x9fa8b110, "pci_bus_read_config_byte" },
	{ 0xd2b09ce5, "__kmalloc" },
	{ 0xf9a482f9, "msleep" },
	{ 0x4c4fef19, "kernel_stack" },
	{ 0xd6ee688f, "vmalloc" },
	{ 0x15692c87, "param_ops_int" },
	{ 0x91eb9b4, "round_jiffies" },
	{ 0x754d539c, "strlen" },
	{ 0x2ec1fa68, "dev_set_drvdata" },
	{ 0x79aa04a2, "get_random_bytes" },
	{ 0xc584b1d3, "dma_set_mask" },
	{ 0x9de6d51e, "napi_complete" },
	{ 0xbbffde9b, "pci_disable_device" },
	{ 0xa5536021, "pci_disable_msix" },
	{ 0x3f140d9f, "netif_carrier_on" },
	{ 0xf89843f9, "schedule_work" },
	{ 0xef83d18f, "netif_carrier_off" },
	{ 0x5da6d1ee, "x86_dma_fallback_dev" },
	{ 0xeae3dfd6, "__const_udelay" },
	{ 0xa9f144bd, "pci_release_regions" },
	{ 0xfb0e29f, "init_timer_key" },
	{ 0x999e8297, "vfree" },
	{ 0x99148172, "pci_bus_write_config_word" },
	{ 0x91715312, "sprintf" },
	{ 0xa528b65b, "__alloc_pages_nodemask" },
	{ 0x7d11c268, "jiffies" },
	{ 0x47ef0d8c, "__netdev_alloc_skb" },
	{ 0x27c33efe, "csum_ipv6_magic" },
	{ 0x98cb0415, "pci_set_master" },
	{ 0xd5f2172f, "del_timer_sync" },
	{ 0xfb578fc5, "memset" },
	{ 0xb7cb648a, "pci_enable_msix" },
	{ 0x84f78440, "pci_restore_state" },
	{ 0xd80c2630, "dev_err" },
	{ 0x27e1a049, "printk" },
	{ 0x449ad0a7, "memcmp" },
	{ 0x2d665932, "free_netdev" },
	{ 0x9166fada, "strncpy" },
	{ 0x665b519b, "register_netdev" },
	{ 0x16305289, "warn_slowpath_null" },
	{ 0x8834396c, "mod_timer" },
	{ 0x4e26d1f6, "netif_napi_add" },
	{ 0xd6b8e852, "request_threaded_irq" },
	{ 0x742eea51, "__get_page_tail" },
	{ 0xc52cf272, "dev_kfree_skb_any" },
	{ 0xa92bbcbc, "contig_page_data" },
	{ 0xc2f2e89d, "pci_find_capability" },
	{ 0xd447f933, "dev_kfree_skb_irq" },
	{ 0x41a58724, "netif_device_attach" },
	{ 0x133f728a, "napi_gro_receive" },
	{ 0x4e5f7514, "_dev_info" },
	{ 0x78764f4e, "pv_irq_ops" },
	{ 0x972841e0, "netif_device_detach" },
	{ 0x42c8de35, "ioremap_nocache" },
	{ 0x8816e55b, "pci_bus_read_config_word" },
	{ 0xb2e21633, "__napi_schedule" },
	{ 0xab0786e4, "eth_type_trans" },
	{ 0x3b02dc27, "pskb_expand_head" },
	{ 0x520b733c, "pci_unregister_driver" },
	{ 0xcc5005fe, "msleep_interruptible" },
	{ 0x50f72e2c, "kmem_cache_alloc_trace" },
	{ 0xe52947e7, "__phys_addr" },
	{ 0x95a39e3a, "pci_set_power_state" },
	{ 0xfcec0987, "enable_irq" },
	{ 0x37a0cba, "kfree" },
	{ 0x69acdf38, "memcpy" },
	{ 0x801678, "flush_scheduled_work" },
	{ 0xb97e03b7, "pci_request_regions" },
	{ 0x4845c423, "param_array_ops" },
	{ 0xf3b95fc1, "dma_supported" },
	{ 0xedc03953, "iounmap" },
	{ 0x4c97f5e5, "__pci_register_driver" },
	{ 0xb2c52452, "put_page" },
	{ 0xc1b91d2e, "unregister_netdev" },
	{ 0x2a44de, "pci_choose_state" },
	{ 0xa93b5657, "__netif_schedule" },
	{ 0x3763c01f, "consume_skb" },
	{ 0xcc56836c, "skb_put" },
	{ 0x4cbf2170, "pci_enable_device" },
	{ 0xca44e780, "dev_get_drvdata" },
	{ 0x9e7d6bd0, "__udelay" },
	{ 0x2bf021e2, "dma_ops" },
	{ 0xf20dabd8, "free_irq" },
	{ 0x8c5ecd7d, "pci_save_state" },
	{ 0x177851cf, "alloc_etherdev_mqs" },
};

static const char __module_depends[]
__used
__attribute__((section(".modinfo"))) =
"depends=";

MODULE_ALIAS("pci:v00008086d000010CAsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001520sv*sd*bc*sc*i*");

MODULE_INFO(srcversion, "584353A987730476BC8E24D");
