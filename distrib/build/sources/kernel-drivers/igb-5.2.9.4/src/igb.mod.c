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
	{ 0xf2dad78a, "device_remove_file" },
	{ 0x5d2dfa6f, "netdev_info" },
	{ 0xeaca354f, "kmalloc_caches" },
	{ 0x9fa8b110, "pci_bus_read_config_byte" },
	{ 0xd2b09ce5, "__kmalloc" },
	{ 0xf9a482f9, "msleep" },
	{ 0x4c4fef19, "kernel_stack" },
	{ 0x9d5d42f7, "pci_enable_sriov" },
	{ 0xd6ee688f, "vmalloc" },
	{ 0x15692c87, "param_ops_int" },
	{ 0x91eb9b4, "round_jiffies" },
	{ 0xfcbe3d9c, "skb_pad" },
	{ 0x2ec1fa68, "dev_set_drvdata" },
	{ 0xd94096de, "kfree_call_rcu" },
	{ 0x2d37342e, "cpu_online_mask" },
	{ 0x79aa04a2, "get_random_bytes" },
	{ 0xc584b1d3, "dma_set_mask" },
	{ 0x9de6d51e, "napi_complete" },
	{ 0xbbffde9b, "pci_disable_device" },
	{ 0xc7a4fbed, "rtnl_lock" },
	{ 0xa5536021, "pci_disable_msix" },
	{ 0x8b8e672b, "hwmon_device_unregister" },
	{ 0x4ea25709, "dql_reset" },
	{ 0x3f140d9f, "netif_carrier_on" },
	{ 0xbed60566, "sub_preempt_count" },
	{ 0xbe1e84be, "pci_disable_sriov" },
	{ 0xf89843f9, "schedule_work" },
	{ 0xc0a3d105, "find_next_bit" },
	{ 0xef83d18f, "netif_carrier_off" },
	{ 0x5da6d1ee, "x86_dma_fallback_dev" },
	{ 0xd8d4121d, "driver_for_each_device" },
	{ 0xeae3dfd6, "__const_udelay" },
	{ 0xfb0e29f, "init_timer_key" },
	{ 0x999e8297, "vfree" },
	{ 0x99148172, "pci_bus_write_config_word" },
	{ 0x91715312, "sprintf" },
	{ 0xa528b65b, "__alloc_pages_nodemask" },
	{ 0x7c15bf12, "netif_napi_del" },
	{ 0x7d11c268, "jiffies" },
	{ 0x47ef0d8c, "__netdev_alloc_skb" },
	{ 0x27c33efe, "csum_ipv6_magic" },
	{ 0x6f5dbb45, "__pskb_pull_tail" },
	{ 0x98cb0415, "pci_set_master" },
	{ 0x87dce889, "dca3_get_tag" },
	{ 0xd5f2172f, "del_timer_sync" },
	{ 0xfb578fc5, "memset" },
	{ 0x70e2ea5f, "pci_enable_pcie_error_reporting" },
	{ 0x2e471f01, "dca_register_notify" },
	{ 0xb7cb648a, "pci_enable_msix" },
	{ 0x84f78440, "pci_restore_state" },
	{ 0x8006c614, "dca_unregister_notify" },
	{ 0xd80c2630, "dev_err" },
	{ 0x27e1a049, "printk" },
	{ 0xc917e655, "debug_smp_processor_id" },
	{ 0xa00aca2a, "dql_completed" },
	{ 0x2d665932, "free_netdev" },
	{ 0x9166fada, "strncpy" },
	{ 0x665b519b, "register_netdev" },
	{ 0x16305289, "warn_slowpath_null" },
	{ 0xcd376e12, "pci_bus_write_config_dword" },
	{ 0x4a37d456, "__pci_enable_wake" },
	{ 0x72c9e303, "dev_close" },
	{ 0x4c6ff041, "add_preempt_count" },
	{ 0x9abf0b33, "netif_set_real_num_rx_queues" },
	{ 0x8834396c, "mod_timer" },
	{ 0x302058df, "netif_set_real_num_tx_queues" },
	{ 0x4e26d1f6, "netif_napi_add" },
	{ 0xd6b8e852, "request_threaded_irq" },
	{ 0x56254ffb, "dca_add_requester" },
	{ 0x43b0c9c3, "preempt_schedule" },
	{ 0x961be3d0, "skb_pull" },
	{ 0x742eea51, "__get_page_tail" },
	{ 0xc52cf272, "dev_kfree_skb_any" },
	{ 0xa92bbcbc, "contig_page_data" },
	{ 0x9f46ced8, "__sw_hweight64" },
	{ 0xe0569b75, "dev_open" },
	{ 0xe523ad75, "synchronize_irq" },
	{ 0xc2f2e89d, "pci_find_capability" },
	{ 0xa2ddaa3c, "device_create_file" },
	{ 0xed12e2ea, "pci_select_bars" },
	{ 0xc6cbbc89, "capable" },
	{ 0x41a58724, "netif_device_attach" },
	{ 0x133f728a, "napi_gro_receive" },
	{ 0x4e5f7514, "_dev_info" },
	{ 0x40a9b349, "vzalloc" },
	{ 0x78764f4e, "pv_irq_ops" },
	{ 0x86e920e0, "__free_pages" },
	{ 0x972841e0, "netif_device_detach" },
	{ 0xf486dda1, "__alloc_skb" },
	{ 0x42c8de35, "ioremap_nocache" },
	{ 0x12a38747, "usleep_range" },
	{ 0x8816e55b, "pci_bus_read_config_word" },
	{ 0xb2e21633, "__napi_schedule" },
	{ 0xa547b942, "pci_bus_read_config_dword" },
	{ 0xd274212b, "pci_cleanup_aer_uncorrect_error_status" },
	{ 0x27d6642f, "kfree_skb" },
	{ 0xab0786e4, "eth_type_trans" },
	{ 0x3b02dc27, "pskb_expand_head" },
	{ 0x3b07ef27, "netdev_err" },
	{ 0x520b733c, "pci_unregister_driver" },
	{ 0xcc5005fe, "msleep_interruptible" },
	{ 0x50f72e2c, "kmem_cache_alloc_trace" },
	{ 0xe52947e7, "__phys_addr" },
	{ 0xf6ebc03b, "net_ratelimit" },
	{ 0x95a39e3a, "pci_set_power_state" },
	{ 0xc8bb95f5, "eth_validate_addr" },
	{ 0xb147bbc6, "pci_disable_pcie_error_reporting" },
	{ 0x37a0cba, "kfree" },
	{ 0x69acdf38, "memcpy" },
	{ 0x801678, "flush_scheduled_work" },
	{ 0x7a6e4d65, "___pskb_trim" },
	{ 0x4845c423, "param_array_ops" },
	{ 0xd6dad00b, "pci_disable_msi" },
	{ 0xf3b95fc1, "dma_supported" },
	{ 0x4a82aa01, "skb_add_rx_frag" },
	{ 0xe4d2838b, "pci_num_vf" },
	{ 0xedc03953, "iounmap" },
	{ 0x31d802ad, "pci_prepare_to_sleep" },
	{ 0x4c97f5e5, "__pci_register_driver" },
	{ 0x2288378f, "system_state" },
	{ 0xb352177e, "find_first_bit" },
	{ 0x46ae0b61, "pci_get_device" },
	{ 0xcc60970c, "dev_warn" },
	{ 0xc1b91d2e, "unregister_netdev" },
	{ 0x28318305, "snprintf" },
	{ 0x84009275, "pci_enable_msi_block" },
	{ 0xa93b5657, "__netif_schedule" },
	{ 0x3763c01f, "consume_skb" },
	{ 0x564cc942, "dca_remove_requester" },
	{ 0xbfd48eaf, "pci_enable_device_mem" },
	{ 0xcc56836c, "skb_put" },
	{ 0xe34ce554, "pci_wake_from_d3" },
	{ 0x44732450, "pci_release_selected_regions" },
	{ 0x54346744, "pci_request_selected_regions" },
	{ 0x75f0e4b1, "skb_copy_bits" },
	{ 0xca44e780, "dev_get_drvdata" },
	{ 0x9d186b93, "hwmon_device_register" },
	{ 0x13a026b8, "pci_find_ext_capability" },
	{ 0x6e720ff2, "rtnl_unlock" },
	{ 0x9e7d6bd0, "__udelay" },
	{ 0x2bf021e2, "dma_ops" },
	{ 0xaf260c92, "device_set_wakeup_enable" },
	{ 0xf20dabd8, "free_irq" },
	{ 0x8c5ecd7d, "pci_save_state" },
	{ 0x177851cf, "alloc_etherdev_mqs" },
};

static const char __module_depends[]
__used
__attribute__((section(".modinfo"))) =
"depends=dca";

MODULE_ALIAS("pci:v00008086d00001F40sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001F41sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001F45sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001533sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001536sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001537sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001538sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d0000157Bsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d0000157Csv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001539sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001521sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001522sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001523sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001524sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d0000150Esv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d0000150Fsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001527sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001510sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001511sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001516sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00000438sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d0000043Asv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d0000043Csv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00000440sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010C9sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d0000150Asv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001518sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010E6sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010E7sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d0000150Dsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001526sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010E8sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010A7sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010A9sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010D6sv*sd*bc*sc*i*");

MODULE_INFO(srcversion, "E377200391EBF74638FEDA2");
